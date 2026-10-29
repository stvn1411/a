---
name: write-product-review
description: Write a new product review page for the TruePicks health site (health.truepicksreview.com) in the house format set by /prodentim-review/ — researched, warm and buyer-friendly but reading as a genuine review, fully SEO'd, linked from the home page and sitemap, and checked at 1920px and 390px. Use for "write a review for <product>", "create the next review", "new blog/article for <product>", "add <product> review page", or any new /<product>-review/ page.
argument-hint: <product name or ClickBank vendor id>
---

# Write a TruePicks product review

The approved model page is **`prodentim-review/index.html`**. Every new review copies its structure, markup, CSS classes, tone and SEO setup. Read it before you start; it is the source of truth when anything here is unclear.

If the user didn't name a product, ask which one (suggest the top `page_status = ok` rows of `data/review-shortlist.csv` that don't have a page yet). Don't guess.

## 1. Pick and check the product
- Find it in `data/review-shortlist.csv`. Use `product_name`, `vendor_id`, `sales_page_url`, `sub_category`, `risk_flag`.
- Only write for rows with `page_status = ok`. If it is `broken`, `unverified` or `check by hand`, tell the user and stop.
- If `risk_flag` is set (disease claim / adult / aggressive weight loss), tell the user before writing; those need extra care with claims.
- Slug: lowercase product name, hyphens, `-review` suffix → folder `<slug>-review/index.html` (e.g. `steel-bite-pro-review/`). Live URL: `https://health.truepicksreview.com/<slug>-review/`.

## 2. Research (never write from memory)
- **Official page** — open the sales page in the built-in browser (prices are usually filled in by JavaScript; curl misses them). Record: ingredient list as stated, servings/days per bottle, every package price, shipping, bonuses, guarantee length, subscription or one-time, "free from" claims. Note the redirect domain if it changes.
- **Policies** — read the refund, shipping and contact pages (usually `/help/refunds.php` etc.). Record: when the refund window starts, what must be returned, who pays return postage, processing time, ClickBank phone, statement descriptor.
- **Evidence** — for each key ingredient, find real human studies on PubMed (WebSearch with `allowed_domains: pubmed.ncbi.nlm.nih.gov`, then WebFetch the abstract). Note authors, year, journal, design, size, result, PubMed ID. Note when the study used a different strain/dose than the product. Use 3–6 sources; every `<sup>` citation must point to one you actually read.
- If a fact can't be verified, leave it out. Don't invent testimonials, ratings, authors, credentials, trial results, customer counts or "we tested it".

## 3. Write the page — section order (match the model page)
1. `<head>`: title, meta description, canonical, robots, OG/Twitter, `article:*` dates, favicon/fonts/CSS with `../` paths, `<script src="../assets/js/analytics.js" async></script>`, JSON-LD.
2. Disclosure bar + site header + nav (copy verbatim, `../` links).
3. Breadcrumb: Home › <Category> (`../#<category-anchor>`) › <Product> Review.
4. `review-head`: eyebrow (e.g. "Oral probiotic review"), H1 `<Product> Review (YEAR): <benefit-led question>?`, dek, byline (TruePicks Review Health Team, last updated, reading time).
5. **Verdict box** (`.verdict`): score circle, "Our verdict in short" (lead with what it does well, one honest qualifier), "A good fit if you" (3–4), "Talk to a doctor/dentist first if you" (2–3), CTA button + note mentioning the guarantee and the date prices were checked.
6. **At a glance** table.
7. **What is <Product> and how is it meant to work?**
8. **Ingredients: what each one does** — table: Ingredient | Why it's included | What the research shows | Evidence badge (`ev-mod` Promising, `ev-low` Mixed/Supporting, `ev-none` Flavour/Limited). Caption: ratings are our summary; note if per-ingredient doses aren't listed.
9. **Does <Product>/<category> work?** — positive findings first, with citations; then a `.callout.info` "What this means for you".
10. **Price: which package is the best value?** — table with total, shipping, supply, cost per day (include shipping); recommend the best-value package and say why.
11. **How the <N>-day money-back guarantee works** — numbered steps from the real policy (start date, what to return, who pays postage, processing time) + `.callout.info` day-before-deadline reminder tip + ClickBank support line.
12. **Pros and cons** — "What we like" (5–7) / "What could be better" (2–3, mild, factual).
13. **How to get the most out of <Product>** — practical numbered tips (official directions + sensible habits).
14. **Is <Product> safe? Side effects** — common mild effects, who should check with a doctor first, FDA line with citation, see-a-professional symptoms.
15. **How <Product> compares with other options**, then a link back to the category on the home page.
16. **How we scored <Product>** — 5 categories, overall = their average (one decimal), e.g. ingredient evidence, ease of use, value for money, guarantee & buying safety, label transparency. Be fair; typical range 3.0–4.0.
17. **FAQ** — 5–6 `<details>`: does it work, is it legit, cost, how long to work, refund, side effects.
18. **Final verdict: is <Product> worth it?** — positive recommendation for the right buyer, best-value package, CTA row (official site + "See other reviews").
19. **Sources** — numbered list with ids `src-*` matching the citations; last item = official site/policies with access date.
20. `review-foot` with "How we review" and "Medical disclaimer" paragraphs (copy from the model page), then the TOC `<aside>`, footer and nav script — all copied from the model page.

## 4. Tone rules (what the user approved)
- Warm, positive and helpful; lead with benefits and who it's a good fit for. It should make a reader comfortable buying — but read like an independent review, not an ad: no hype words ("miracle", "revolutionary", "secret"), no fake urgency, no ALL-CAPS, no exclamation marks.
- **Do not add an in-article disclosure box** (no "We are not paid by…" / "we bought nothing" / "information only" notice at the top of the article). The user removed it from the model page. Keep only what the model page has: the site-wide disclosure bar, the `review-foot` paragraphs and the footer.
- Keep these material facts, stated briefly and neutrally (they protect buyers and the site's Google standing): no trials on the finished product (if true), refund conditions (what to return, who pays postage, window start), doses not disclosed (if true), and who should see a doctor/dentist first. Never say it cures, treats or prevents a disease.
- Use US spelling for prices/units as on the model page; keep paragraphs short.

## 5. Links and SEO
- Official links: `href="<official homepage>" target="_blank" rel="nofollow noopener" data-offer="<slug>"`. Use the affiliate hoplink only when the user says to switch; then use `rel="sponsored nofollow noopener"`.
- `<title>` ≤ 60 characters, pattern `<Product> Review YEAR: <2–4 keywords>`; meta description 140–155 characters; one H1; canonical = `https://health.truepicksreview.com/<slug>-review/`.
- JSON-LD `@graph` with `BreadcrumbList`, `Review` (`reviewRating` = overall score, `positiveNotes`/`negativeNotes` = the pros/cons, `itemReviewed` Product with name/brand/category/description/url) and `FAQPage` whose questions and answers match the visible FAQ word for word.
- Internal links: breadcrumb, category link, "See other reviews".

## 6. Wire it into the site
- `index.html`: point the product's card at `<slug>-review/` (add a card in the right category if missing), set its status line to `Our score: X.X / 5 · Updated <Mon D, YYYY>`, and make sure the home JSON-LD `ItemList` has the `-review/` URL.
- `sitemap.xml`: add `<url><loc>https://health.truepicksreview.com/<slug>-review/</loc><lastmod>YYYY-MM-DD</lastmod></url>`.

## 7. Verify before saying it's done
1. Run `python3 -I .claude/skills/write-product-review/check_review.py <slug>-review` from the repo root and fix every FAIL.
2. Screenshot the real `file://` URL at 1920px with headless Chrome (isolated `--user-data-dir`).
3. Check 390px in the browser pane over a local server (`python3 -m http.server 8765 -d <repo>` in the background, open `http://localhost:8765/<slug>-review/`): `document.documentElement.scrollWidth` must equal `innerWidth`; wide tables may scroll inside `.table-wrap`.
4. Report what was checked, prices with the date checked, and anything unverified. Don't commit unless the user asks; commit locally only, never push.
