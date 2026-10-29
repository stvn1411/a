"""Check a review page against the TruePicks house format.

Usage (from the repo root): python3 -I .claude/skills/write-product-review/check_review.py <slug>-review
"""
import html
import json
import re
import sys
from pathlib import Path

SITE = "https://health.truepicksreview.com"
REQUIRED_SECTIONS = ["at-a-glance", "what-is-it", "ingredients", "research", "price", "refund",
                     "pros-cons", "how-to-use", "safety", "alternatives", "scoring", "faq",
                     "final-verdict", "sources"]
BANNED = [r"we are not paid by", r"we bought nothing", r"\bmiracle\b", r"\brevolutionary\b",
          r"\b(cures|can cure|will cure)\b", r"\bguaranteed results\b", r"!\s*<"]

folder = sys.argv[1].strip("/")
repo = Path.cwd()
page = repo / folder / "index.html"
results = []


def check(ok, label, detail=""):
    results.append((ok, label, detail))


if not page.exists():
    sys.exit(f"FAIL  {page} not found")
s = page.read_text(encoding="utf-8")
text = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S))

check(folder.endswith("-review"), "folder ends with -review", folder)

title = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1))
check(len(title) <= 60, "title <= 60 chars", f"{len(title)}: {title}")
m = re.search(r'<meta name="description" content="(.*?)"', s)
desc = html.unescape(m.group(1)) if m else ""
check(120 <= len(desc) <= 160, "meta description 120-160 chars", str(len(desc)))
check(s.count("<h1") == 1, "exactly one <h1>")
check(f'<link rel="canonical" href="{SITE}/{folder}/">' in s, "canonical matches folder")
check('<script src="../assets/js/analytics.js" async></script>' in s, "GA analytics script included")
check('href="../assets/css/main.css"' in s, "shared stylesheet linked")

blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
graph = []
try:
    for b in blocks:
        graph += json.loads(b).get("@graph", [])
    check(bool(graph), "JSON-LD parses")
except json.JSONDecodeError as e:
    check(False, "JSON-LD parses", str(e))
types = {g.get("@type") for g in graph}
for t in ("BreadcrumbList", "Review", "FAQPage"):
    check(t in types, f"JSON-LD has {t}")

review = next((g for g in graph if g.get("@type") == "Review"), {})
rating = review.get("reviewRating", {}).get("ratingValue")
check(rating and f'aria-label="Our score: {rating} out of 5"' in s, "schema rating matches score badge", str(rating))
rows = re.findall(r"<tr><td>[^<]+</td><td>[^<]+</td><td>([\d.]+) / 5</td></tr>", s)
if rows:
    avg = round(sum(map(float, rows)) / len(rows), 1)
    check(rating and abs(avg - float(rating)) < 0.051, "overall score = average of categories", f"avg {avg} vs {rating}")
else:
    check(False, "scoring table found")

faq = next((g for g in graph if g.get("@type") == "FAQPage"), {})
schema_q = [q["name"] for q in faq.get("mainEntity", [])]
visible_q = [html.unescape(q) for q in re.findall(r"<summary>(.*?)</summary>", s)]
check(schema_q == visible_q and len(schema_q) >= 5, "FAQ schema matches visible FAQ (5+)", f"{len(schema_q)} vs {len(visible_q)}")

ids = set(re.findall(r'id="([^"]+)"', s))
missing = [x for x in REQUIRED_SECTIONS if x not in ids]
check(not missing, "all house-format sections present", ", ".join(missing))
broken = [h for h in re.findall(r'href="#([^"]+)"', s) if h not in ids]
check(not broken, "in-page anchors resolve", ", ".join(broken))
cites = set(re.findall(r'href="#(src-[^"]+)"', s))
check(cites and cites <= ids, "every citation has a source entry", ", ".join(sorted(cites - ids)))

offers = re.findall(r'<a [^>]*data-offer="[^"]+"[^>]*>', s)
check(len(offers) >= 2, "2+ official-site buttons with data-offer", str(len(offers)))
check(all('rel="nofollow noopener"' in a or 'rel="sponsored nofollow noopener"' in a for a in offers),
      "official links are nofollow (sponsored if affiliate)")

check('class="notice"' not in s, "no in-article disclosure box")
hits = [p for p in BANNED if re.search(p, s, re.I)]
check(not hits, "no banned phrases / hype", ", ".join(hits))

site_pages = ["about", "affiliate-disclosure", "privacy-policy", "terms", "contact"]
missing_links = [p for p in site_pages if f'href="../{p}/"' not in s]
check(not missing_links, "links to About, Affiliate disclosure, Privacy, Terms, Contact", ", ".join(missing_links))
missing_pages = [p for p in site_pages if not (repo / p / "index.html").exists()]
check(not missing_pages, "site pages exist", ", ".join(missing_pages))

home = (repo / "index.html").read_text(encoding="utf-8")
check(f'href="{folder}/"' in home, "linked from home page")
check(f"{SITE}/{folder}/" in home, "in home page JSON-LD ItemList")
sitemap = (repo / "sitemap.xml").read_text(encoding="utf-8")
check(f"<loc>{SITE}/{folder}/</loc>" in sitemap, "listed in sitemap.xml")

words = len(text.split())
check(words >= 1500, "length >= 1500 words", str(words))

fails = 0
for ok, label, detail in results:
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {label}" + (f"  ({detail})" if detail else ""))
print(f"\n{len(results) - fails}/{len(results)} checks passed")
sys.exit(1 if fails else 0)
