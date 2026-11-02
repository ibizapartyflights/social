# Web guide generator (ibizapartyflights.co.uk)

The live site lives in the GitHub repo `ibizapartyflights/Web` (Netlify deploys every push to `main`, 15 credits each — one push per week max).

- `build.py` – page template: header, consent, Cloudflare Web Analytics, JSON-LD (Article, Breadcrumb, FAQ), affiliate helpers `tp()`, `bk()`, `cta()`.
- `guide.css` – shared guide styles.
- `content.py` – the six original guides plus the guides index. To add a guide, append a tuple to `pages` and rerun with `OUT=/path/to/Web/guides python3 content.py`.

After adding a guide also:
1. Add its URL with today's `<lastmod>` to `sitemap.xml` in the Web repo.
2. Optionally add a card to the `#guides` section in `index.html` (keep 6 cards max; newest first).

Rules: British English; facts only if sure (no invented prices, line numbers or 2027 dates); affiliate disclosure stays; never promote drink-driving; no club logos; "cheapest"/"best deals" claims banned.
