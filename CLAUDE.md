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

## Publishing plan: 3 reviews per branch, write everything first, merge later
`data/publishing-plan.csv` is the plan (built by `data/build_publishing_plan.py`; once branches exist, edit the CSV
by hand instead of re-running it). It puts the 337 planned reviews into `productlist-1` … `productlist-113`, 3 per
branch, ordered by wave (A high priority → E low priority with risk flag) and grouped by topic so the 3 reviews in a
branch can link to each other.

How we work:
1. **Write all branches first.** Go through the plan in order: `productlist-1`, then `-2`, `-3`, … Each branch holds
   exactly the products the CSV lists for it (`branch` column, in `order`): 3 each, only `productlist-113` has 1.
2. **Branches are stacked.** `productlist-1` is cut from `main`; every later branch is cut from the previous one
   (`productlist-N` from `productlist-(N-1)`). This is why the shared files (`index.html`, `sitemap.xml`,
   the CSV) never conflict.
3. **The user merges PRs from time to time, in order.** The CSV's `merge_week` (2 branches a week) is a guide, not
   a deadline. One PR per branch; its base is the previous branch (`productlist-1`'s base is `main`), so each PR
   shows only its own 3 reviews. When a PR is merged and its branch deleted, GitHub retargets the next PR to `main`.
   PRs must be merged with **"Create a merge commit"**: squash or rebase merges break the stack.

### Writing one branch
```bash
git fetch origin
```
- Next branch = one after the highest `productlist-N` on origin (`git branch -r --list 'origin/productlist-*'`).
  Cut it from that branch: `git switch -c productlist-N origin/productlist-(N-1)` (or `origin/main` for N=1).
- For each of its 3 products, use the **`write-product-review` skill** (`.claude/skills/write-product-review/`):
  research, write in the ProDentim format, wire into `index.html` and `sitemap.xml`, pass `check_review.py`, check
  1920px and 390px. No in-article disclosure box. Every review is positive and scores **4.5–5.0** overall.
- If `name_check` says "rename before writing", fix `product_name` and `page_slug` in the CSV first (the name is
  still a marketplace title). Wave C/E rows have a `risk_flag` (disease, adult, aggressive weight-loss claims):
  keep claims cautious and neutral.
- Link the 3 reviews in the branch to each other where it's natural (same topic).
- One commit per review, then set the 3 rows' `status` to `in-pr` in the CSV in the last commit.
- Push: `git push -u origin productlist-N`. In this batch workflow, pushing the branch is expected (this overrides
  the skill's "never push"); never push to `main` and never force-push a branch that already has a PR.
- Give the user the PR link: `https://github.com/stvn1411/a/compare/productlist-(N-1)...productlist-N?expand=1`
  (for N=1: `main...productlist-1`), and what was checked.

### Fixing an older branch
If a review in `productlist-K` needs a change after later branches exist: commit the fix on `productlist-K`, then
merge it forward through every later branch (`K+1` from `K`, `K+2` from `K+1`, …) and push each. Don't rebase pushed
branches.

### After merges
Branches merged into `main` are live. When asked to sync status: `git fetch origin --prune`, find merged branches
(`git branch -r --merged origin/main --list 'origin/productlist-*'`, or ones GitHub already deleted), set their rows to
`published` in the CSV on the next branch being written.

## Other notes
- Everything must stay free (no paid tools or plans). GA4 is loaded site-wide by `assets/js/analytics.js`; every new
  page must include it.
- `data/clickbank-health-products.csv` (437 products) → `data/review-shortlist.csv` (350 verified) →
  `data/publishing-plan.csv`.
