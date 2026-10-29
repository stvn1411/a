"""Build data/publishing-plan.csv: which product review goes into which productlist-N branch.

Run from the repo root: python3 -I data/build_publishing_plan.py
Re-run after the shortlist changes; branches already marked done in DONE keep their place only if you
also keep the order rules the same, so prefer editing the CSV by hand once branches have started.
"""
import csv
import re
from pathlib import Path

PER_BRANCH = 3
BRANCHES_PER_WEEK = 2
DONE = {"PRODENTIM": "prodentim-review"}  # already published on main

# Waves, in publishing order. Risk = disease / adult / aggressive weight-loss claims (needs extra care).
WAVES = [
    ("A", "High priority", lambda r: r["priority"].startswith("1") and not r["risk_flag"]),
    ("B", "Medium priority", lambda r: r["priority"].startswith("2") and not r["risk_flag"]),
    ("C", "High/Medium with risk flag", lambda r: r["priority"][0] in "12" and r["risk_flag"]),
    ("D", "Low priority", lambda r: r["priority"].startswith("3") and not r["risk_flag"]),
    ("E", "Low priority with risk flag", lambda r: r["priority"].startswith("3") and r["risk_flag"]),
]

# Topic from name/title/category, ordered from most to least specific. Second value = home page category anchor.
TOPICS = [
    ("Dental & oral", "oral-health", r"dent|tooth|teeth|\bgums?\b|\boral\b|\bbite\b|bad breath|smile"),
    ("Hearing & balance", "hearing-brain", r"\bhear(ing)?\b|\bears?\b|sharpear|tinnitus|audi|quietum|sonic|sonovive|echoxen|vertigo|vertiaid|dizz|claritox"),
    ("Vision & eye", "hearing-brain", r"vision|\beyes?\b|eyesight|visiflora|igenics|floaters"),
    ("Brain & memory", "hearing-brain", r"brain|memory|neuro|cogni|\bmind|focus|pineal|memo|cortex|synap|lion's mane"),
    ("Blood sugar", "blood-sugar", r"gluco|blood sugar|sugar defender|diabet|insulin|glyco"),
    ("Women's health", "mens-health", r"women|female|femi|menopaus|pelvic|vagin|intimacy|fibroid|ovarian|yeast"),
    ("Prostate & urinary", "mens-health", r"prosta|urin|bladder|\bbph\b|viriflow|titanflow|flowforce|\bpee\b"),
    ("Men's performance", "mens-health", r"\bmale\b|men's|testost|alpha|erect|\bed\b|stamina|vigor|virility|nitric|\bstud\b|potent|endopeak|enlarg|bedroom|pleasure"),
    ("Joints & pain", "gut-skin", r"joint|knee|\bhips?\b|back pain|pain|shoulder|arthrit|flexi|sciatic|\bneck\b|posture|spine|mobility"),
    ("Heart & circulation", "gut-skin", r"heart|cardio|blood pressure|cholest|circulat|arter|veno|cholibrium"),
    ("Nerves", "gut-skin", r"nerve|neuropath|nervo"),
    ("Skin, hair & nails", "gut-skin", r"\bskin|nail|\bhair|fung|derma|collagen|cellulite|skin tag|acne|eczema|kera"),
    ("Gut & digestion", "gut-skin", r"\bgut\b|digest|biome|bloat|constipat|probiot|liver|hepato|colon|poop"),
    ("Weight management", "weight-management", r"weight|slim|burn|\blean|\bfat\b|belly|keto|\bdiets?\b|metabo|appetite|\btea\b|java|liv pure|sculpt|ikaria|lymph|water retention|venus factor"),
    ("Sleep & stress", "hearing-brain", r"sleep|insomnia|\bcalm|stress|anxiety|relax"),
    ("Lungs & breathing", "gut-skin", r"lung|breathe|pulmo"),
    ("Fitness & exercise", "weight-management", r"workout|fitness|muscle|training|abs\b|pull-?up|stretch|yoga|exercise"),
]

# Last resort when name, title and vendor pitch don't reveal the topic.
SUBCATEGORY_TOPIC = {
    "Diets & Weight Loss": ("Weight management", "weight-management"),
    "Dental Health": ("Dental & oral", "oral-health"),
    "Men's Health": ("Men's performance", "mens-health"),
    "Women's Health": ("Women's health", "mens-health"),
    "Sleep and Dreams": ("Sleep & stress", "hearing-brain"),
    "Mental Health": ("Brain & memory", "hearing-brain"),
    "Beauty": ("Skin, hair & nails", "gut-skin"),
    "Exercise & Fitness": ("Fitness & exercise", "weight-management"),
}

# Vendor pitch text from the full ClickBank list, used as a second pass.
PITCH = {r["vendor_id"]: r["vendor_pitch"] for r in csv.DictReader(open("data/clickbank-health-products.csv", encoding="utf-8-sig"))}


def match(text):
    for name, anchor, pat in TOPICS:
        if re.search(pat, text):
            return name, anchor
    return None


def topic(r):
    # sub_category is only a fallback: "Dietary Supplements" would otherwise match the weight rule.
    return (match(" ".join([r["product_name"], r["marketplace_title"]]).lower())
            or match(PITCH.get(r["vendor_id"], "").lower())
            or SUBCATEGORY_TOPIC.get(r["sub_category"])
            or ("General wellness", "gut-skin"))


def name_check(name):
    # Product names come from marketplace titles; flag ones that are still marketing text.
    if len(name) > 30 or re.search(r"[()%$]|^[a-z]", name):
        return "rename before writing"
    if re.search(r"commission|offer|\.com|\bepc\b|\bvsl\b|\bcb\b", name, re.I):
        return "rename before writing"
    return ""


def slug(name):
    s = re.sub(r"[®™]", "", name.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s + "-review"


rows = list(csv.DictReader(open("data/review-shortlist.csv", encoding="utf-8-sig")))
ok = [r for r in rows if r["page_status"] == "ok" and r["vendor_id"] not in DONE]
hold = [r for r in rows if r["page_status"] in ("unverified", "check by hand")]
skip = [r for r in rows if r["page_status"] == "broken"]
for r in ok:
    r["topic"], r["home_anchor"] = topic(r)

batches = []
carry = []  # a wave's last, short batch is completed from the start of the next wave
for wave, wave_name, rule in WAVES:
    pool = sorted([r for r in ok if rule(r)], key=lambda r: -float(r["score"]))
    for r in pool:
        r["wave_label"] = f"{wave} - {wave_name}"
    while pool:
        # Start each branch with the best remaining product, then fill with the best same-topic products
        # from this wave, so each branch is a themed set that can link to each other.
        batch = carry or [pool.pop(0)]
        carry = []
        same = [r for r in pool if r["topic"] == batch[0]["topic"]]
        for r in same[: PER_BRANCH - len(batch)]:
            batch.append(r)
            pool.remove(r)
        while len(batch) < PER_BRANCH and pool:
            batch.append(pool.pop(0))
        if len(batch) < PER_BRANCH:
            carry = batch
        else:
            batches.append(batch)
if carry:
    batches.append(carry)

plan = []
for branch_no, batch in enumerate(batches, 1):
    for i, r in enumerate(batch, 1):
        plan.append({
            "branch": f"productlist-{branch_no}",
            "merge_week": (branch_no - 1) // BRANCHES_PER_WEEK + 1,
            "order": i,
            "wave": r["wave_label"],
            "priority": r["priority"],
            "score": r["score"],
            "product_name": r["product_name"],
            "page_slug": slug(r["product_name"]),
            "name_check": name_check(r["product_name"]),
            "topic": r["topic"],
            "home_category": "#" + r["home_anchor"],
            "risk_flag": r["risk_flag"],
            "why": r["why"],
            "gravity": r["gravity"],
            "product_type": r["product_type"],
            "sales_page_url": r["sales_page_url"],
            "vendor_id": r["vendor_id"],
            "status": "planned",
        })

for vid, folder in DONE.items():
    r = next(x for x in rows if x["vendor_id"] == vid)
    plan.insert(0, {"branch": "main (published)", "merge_week": 0, "order": 1, "wave": "Done",
                    "priority": r["priority"], "score": r["score"], "product_name": r["product_name"],
                    "page_slug": folder, "name_check": "", "topic": topic(r)[0], "home_category": "#" + topic(r)[1],
                    "risk_flag": r["risk_flag"], "why": r["why"], "gravity": r["gravity"],
                    "product_type": r["product_type"], "sales_page_url": r["sales_page_url"],
                    "vendor_id": vid, "status": "published"})
for r, label in [(x, "hold - verify sales page first") for x in hold] + [(x, "skip - sales page broken") for x in skip]:
    plan.append({"branch": "not scheduled", "merge_week": "", "order": "", "wave": "Not scheduled",
                 "priority": r["priority"], "score": r["score"], "product_name": r["product_name"],
                 "page_slug": slug(r["product_name"]), "name_check": "", "topic": "", "home_category": "",
                 "risk_flag": r["risk_flag"], "why": r["why"], "gravity": r["gravity"],
                 "product_type": r["product_type"], "sales_page_url": r["sales_page_url"],
                 "vendor_id": r["vendor_id"], "status": label})

with open("data/publishing-plan.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(plan[0].keys()))
    w.writeheader()
    w.writerows(plan)
print(f"{branch_no} branches, {sum(1 for p in plan if p['status']=='planned')} planned reviews, "
      f"{(branch_no + BRANCHES_PER_WEEK - 1) // BRANCHES_PER_WEEK} weeks")
