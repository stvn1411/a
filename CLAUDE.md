# truepicks-sites

Static health review site for **https://health.truepicksreview.com/** (GitHub Pages from `main`, custom domain in `CNAME`).
Each product review is its own folder: `<slug>-review/index.html`. `prodentim-review/` is the approved model page.

This file wins where `README.md` disagrees: the README's "planning only / not pushed / Astro or Hugo" sections are
out of date.

## Git and GitHub account
- Repo: `stvn1411/a`, remote `origin` = `git@github-truepicks:stvn1411/a.git` (SSH alias with this project's own key).
- Commit only as `stvn1411 <steve1223344556@gmail.com>` (already set in this repo's local git config). Never use
  another identity, and never push through `github.com` directly.
- No `Co-Authored-By` trailer in commit messages and no "Generated with Claude Code" line in PR descriptions.
- `gh` on this machine is logged in to a different account: don't use it here. The user opens PRs on github.com.

## Publishing plan: 3 reviews per branch, every branch independent
`data/publishing-plan.csv` is the plan (built by `data/build_publishing_plan.py`). It puts the 337 planned reviews into
`productlist-1` … `productlist-113`, 3 per branch (only `productlist-113` has 1), ordered by wave (A high priority →
E low priority with risk flag) and grouped by topic so the 3 reviews in a branch can link to each other.

How we work (changed 2026-10-29; replaces the old stacked-branch plan):
1. **Every branch is cut from `main` and only adds its own review folders.** A branch contains nothing but
   `<slug>-review/index.html` for its products (plus images inside those folders if any).
2. **Don't touch shared files in review branches:** `index.html`, `sitemap.xml`, `assets/`, the shared site pages
   (`about/` etc.), `data/` (including the plan CSV) and `CLAUDE.md`/skills. That way no two PRs ever conflict.
3. **PRs are independent.** Base is always `main`; the user merges them in any order, from time to time.
4. **`main` stays out of date on purpose.** About once a month the user asks for a "common update" on `main`: add
   every review folder now on `main` to `index.html` (cards + JSON-LD `ItemList`) and `sitemap.xml`, and set their
   rows to `published` in the CSV. Until then new reviews are reachable only by URL and their sister reviews.

### Writing one branch
```bash
git fetch origin
```
- Pick the branch: the user names it, or take the lowest `productlist-N` that has no branch on origin yet
  (`git branch -r --list 'origin/productlist-*'`).
- `git switch -c productlist-N origin/main`
- For each product in it (CSV `branch` column, in `order`), use the **`write-product-review` skill**: research,
  write in the ProDentim format, pass `check_review.py` (standalone mode, the default), check 1920px and 390px. No
  in-article disclosure box. Every review is positive and scores **4.5–5.0** overall.
- If `name_check` says "rename before writing", choose a clean product name and slug and tell the user (don't edit
  the CSV in the branch; it is fixed in the monthly common update). Wave C/E rows have a `risk_flag` (disease, adult,
  aggressive weight-loss claims): keep claims cautious and neutral.
- Links from a review may go only to pages that exist on `main` or to the other reviews in the same branch (link the
  3 to each other where it's natural). Never link to a review that is only in another unmerged branch.
- One commit per review. Check `git diff --stat origin/main` shows only the new review folders.
- Push: `git push -u origin productlist-N`. Pushing review branches is expected (this overrides the skill's "never
  push"); never push to `main` unless the user asks.
- Give the user the PR link `https://github.com/stvn1411/a/compare/main...productlist-N?expand=1` and what was
  checked. Merge method doesn't matter now.

### Monthly common update (only when the user asks, on `main`)
`git fetch origin --prune`, then for every `*-review/` folder on `main` that isn't wired yet: add its home page card
(right category, `Our score: X.X / 5 · Updated <date>`), add it to the home JSON-LD `ItemList` and `sitemap.xml`, and
set its CSV row to `published` (fix any renamed names/slugs there too). Run `check_review.py --wired <folder>` for
each; all must pass.

## Other notes
- Everything must stay free (no paid tools or plans). GA4 is loaded site-wide by `assets/js/analytics.js`; every new
  page must include it.
- `data/clickbank-health-products.csv` (437 products) → `data/review-shortlist.csv` (350 verified) →
  `data/publishing-plan.csv`.
