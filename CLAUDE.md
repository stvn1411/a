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

## Publishing plan: batches of 3, one Claude session per batch, all in parallel
**`data/batches.csv`** is the work list: one row per batch, 113 batches. Batch N = branch `productlist-N` with 3
products (only batch 113 has 1), their slugs, wave, topics and notes (rename flags, risk flags). Batches are ordered
by wave (A high priority → E low priority with risk flag) and grouped by topic so the 3 reviews can link to each
other. `data/publishing-plan.csv` has the same plan with one row per product and full details (sales page URL,
vendor id, score). Both are built by `data/build_publishing_plan.py`.

How we work (changed 2026-10-29):
1. **Several Claude sessions run at the same time, each on a different batch.** A session claims its batch first
   with `data/claim_batch.py` (below), so two sessions can never take the same one.
2. **Every batch branch is cut from `main` and only adds its own review folders** (`<slug>-review/index.html`, plus
   images inside those folders if any).
3. **Don't touch shared files in batch branches:** `index.html`, `sitemap.xml`, `assets/`, the shared site pages
   (`about/` etc.), `data/` and `CLAUDE.md`/skills. That way no two PRs ever conflict.
4. **PRs are independent.** Base is always `main`; the user merges them in any order, from time to time.
5. **`main` stays out of date on purpose.** About once a month the user asks for a "common update" on `main`: add
   every review folder now on `main` to `index.html` (cards + JSON-LD `ItemList`) and `sitemap.xml`, and set their
   rows to `published` in the CSVs. Until then new reviews are reachable only by URL and their sister reviews.

### Working on one batch (each session)
1. **Claim the batch** from any checkout of this repo:
   ```bash
   python3 -I data/claim_batch.py
   ```
   (or `python3 -I data/claim_batch.py 7` when the user names batch 7). It fetches origin, skips batches whose branch
   exists on origin or whose reviews are already on `main`, and claims one by pushing `productlist-N` as a single
   empty "Start batch N" commit on top of `origin/main`. The push only succeeds if the branch doesn't exist yet, so if
   two sessions race, one wins and the other takes the next batch. It prints the 3 products and slugs. If it says the
   batch isn't free, tell the user; never work on a batch you didn't claim.
2. **Work in your own folder.** Never switch branches in a checkout another session may be using.
   - If this session already runs in its own git worktree (the desktop app can create one per session):
     `git fetch origin && git switch productlist-N`.
   - Otherwise create one: `git worktree add ../truepicks-worktrees/productlist-N productlist-N` and do all work,
     checks and commits there. The repo's local git config (stvn1411 identity) and the `origin` remote apply there too.
3. **Write the 3 reviews** with the **`write-product-review` skill**: research, write in the ProDentim format, pass
   `check_review.py` (standalone mode, the default), check 1920px and 390px. For the 390px check use port
   `8700 + N` and your own Chrome profile, and only stop processes you started. No in-article disclosure box. Every
   review is positive and scores **4.5–5.0** overall.
   - If the notes say "rename before writing", choose a clean product name and slug and tell the user (don't edit
     the CSVs in the branch; they are fixed in the monthly common update). Risk-flagged products (disease, adult,
     aggressive weight-loss claims): keep claims cautious and neutral.
   - Links may go only to pages that exist on `main` or to the other reviews in the same batch (link the 3 to each
     other where it's natural). Never link to a review that is only in another unmerged branch.
4. **Commit and push:** one commit per review. Check `git diff --stat origin/main` shows only the batch's review
   folders, then `git push origin productlist-N` (push often; never force-push, never push to `main` unless the user
   asks). Pushing batch branches is expected (this overrides the skill's "never push").
5. **Hand over:** give the user the PR link `https://github.com/stvn1411/a/compare/main...productlist-N?expand=1`
   and what was checked. When the user is done with the worktree: `git worktree remove ../truepicks-worktrees/productlist-N`.

If a session gives up on a batch before committing any review, release it so another session can take it:
`git push origin --delete productlist-N`. Never delete a branch that has review commits.

To see which batches are taken: `git ls-remote --heads origin 'productlist-*'`.

### Monthly common update (only when the user asks, on `main`)
`git fetch origin --prune`, then for every `*-review/` folder on `main` that isn't wired yet: add its home page card
(right category, `Our score: X.X / 5 · Updated <date>`), add it to the home JSON-LD `ItemList` and `sitemap.xml`, and
set its rows to `published` in `data/publishing-plan.csv` (fix any renamed names/slugs there and in
`data/batches.csv` too). Run `check_review.py --wired <folder>` for
each; all must pass.

## Other notes
- Everything must stay free (no paid tools or plans). GA4 is loaded site-wide by `assets/js/analytics.js`; every new
  page must include it.
- `data/clickbank-health-products.csv` (437 products) → `data/review-shortlist.csv` (350 verified) →
  `data/publishing-plan.csv` + `data/batches.csv`.
