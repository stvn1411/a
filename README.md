# truepicks-sites

**Status:** planning only. Local repo, **not pushed anywhere**, no remote configured. Created 2026-10-28.

## Goal
One repository that holds **all our affiliate product pages** (ClickBank offers and similar), served as a fast static
site on our own domain, so that Pinterest pins (and later other channels) can send people to a useful, indexable page.

The pins come from the sibling project `../secret-pin` (affirmation pins scheduled on Pinterest, linking to
`https://manifestation.truepicksreview.com/`). This repo is where those links should eventually land.

## What we will build
- A static site generated from **markdown/data files** (one file per product), so adding a product = add a file and push.
- **One folder (URL) per product**, e.g. `/<niche>/<product>/`. Each page is its own indexable URL and can rank on its own.
- Shared templates, so Claude can generate and update many pages consistently.
- Per-niche sections (manifestation first, more niches later) inside the same repo.

## Planned structure (to confirm before building)
```
truepicks-sites/
  README.md
  content/                 # one markdown file per product / guide (title, summary, pros/cons, FAQ, affiliate link)
  data/products.json       # product list: name, niche, slug, affiliate link, vendor, notes
  src/                     # templates and layout (Astro or Hugo - decision below)
  public/                  # static files: robots.txt, CNAME (custom domain), images
  .github/workflows/       # build + deploy workflow
```

## Decisions still open
1. **Generator:** Astro (more flexible) or Hugo (simpler, faster builds). Both turn markdown into static pages.
2. **Domain layout:** keep `manifestation.truepicksreview.com` (subdomain) or use paths on the main domain
   (`truepicksreview.com/<niche>/...`). Pick one and keep it - changing later needs redirects for every page.
3. **Hosting:** GitHub Pages today. See the risk below; Cloudflare Pages is the fallback.
4. **First products:** list of the first 5-10 offers (name + affiliate link) to build pages for.
5. **Private repo vs Pages:** whether publishing a site from a *private* repo needs a paid GitHub plan - to check before pushing.

## Content rules (so pages can rank)
- Every page must add value beyond the vendor's sales page: who it is for / not for, honest pros and cons, FAQ, comparison.
- No thin pages (a blurb + a link), no bulk near-duplicate pages, no income or medical claims.
- Disclose affiliate links clearly near the top of each page ("affiliate link - we may earn a commission").
- Also publish a few genuine helpful guides that link to the product pages; the site should still make sense without the links.
- Each product must be checked against its vendor's affiliate agreement and ClickBank's rules before promoting it.

## SEO checklist (do when the site goes live)
- Use the custom domain, canonical URL on every page, one URL style (trailing slash) everywhere.
- Generate `sitemap.xml`; add `robots.txt`; link every page from the homepage or a category page.
- Verify the site in **Google Search Console** and **Bing Webmaster Tools** (HTML-tag method works on GitHub Pages).
- Fast, mobile-friendly pages; unique title and description per page.

## Hosting notes
- GitHub Pages: one site per repo, **one custom domain per repo**, unlimited pages inside the site.
  Limits: site up to 1 GB, soft 100 GB/month bandwidth, soft 10 builds/hour (not applied when deploying with a GitHub Actions workflow).
- **Risk:** GitHub says Pages is not meant for, or allowed as, free hosting for an online business or a site mainly aimed at
  commercial transactions. An affiliate site may be a grey area. If it is taken down, move the static files to Cloudflare Pages
  (check its terms first) and change DNS at Namecheap.
- Do not use Vercel's free (Hobby) plan: it is non-commercial only and lists affiliate linking as a commercial use.
- DNS is at **Namecheap** (Advanced DNS): add a CNAME for the subdomain pointing to `<github-username>.github.io`; remove old
  conflicting records first.

## Rules for this repo
- Keep it private and local until we decide otherwise. **Do not push without explicit approval.**
- Do not commit secrets or account passwords. Affiliate links are fine (kept in `data/products.json`).

## Next steps
- [ ] Decide generator and domain layout (open decisions 1-2)
- [ ] Choose the first 5-10 products
- [ ] Scaffold the site, one product page template, sitemap, robots, canonical tags
- [ ] Write real content for the first pages
- [ ] Local preview and review
- [ ] Decide on hosting and publish (needs approval)
