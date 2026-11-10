# SOCOR redesign

A separate static recreation. SOCOR’s original domain and hosting have not been changed.

## GitHub Pages

Published separately at https://jay-rtl.github.io/socor/ using the `main` branch and `/docs` directory.

Run `npm run build:pages` after source changes, then commit both source and `docs/`. The build rewrites local absolute URLs for the `/socor/` base path. The default `npm run build` still produces root-hosted output in `dist/`.

## Run and verify

- `npm run dev` serves http://localhost:3000 with clean page URLs and a custom 404.
- `npm run build` packages the public site in `dist/`, excluding audit files and tests.
- `npm run lint` checks JavaScript syntax with Node.
- `npm test` checks all 11 pages, titles/descriptions, heading order, IDs, internal links/fragments, image alternatives/dimensions and local assets.
- With the preview server running, `npm run test:browser` runs Chromium/Playwright interaction and accessibility checks. It uses the existing system Chromium and the test-only axe-core copy in `audit/`. Set `SOCOR_TEST_URL` to use another local preview origin.

The six main routes and five service detail routes have real index.html files. Static hosting must resolve directory indexes and use 404.html for unknown routes. Five original /new-* routes redirect to the corresponding new destinations. No production hosting configuration was changed.

## Content sources

Company facts, contacts and inventory were retrieved from https://socorconstruction.com/ and /new-about/, /new-projects/, /new-products-services/, /new-equipment/, /new-contact-us/ on November 11, 2026 (Singapore date).

Authentic SOCOR photographs are stored as WebP. Project titles follow descriptive source filenames; no completion dates, clients or contract scopes were invented. Original homepage product imagery did not consistently match its labels, so plant photographs are used as contextual operations imagery.

PCAB and ISO claims are published corporate history; current validity remains unverified. Equipment quantities and capacities follow SOCOR’s full 42-row published inventory; current availability must be confirmed. Barlow Condensed and DM Sans are self-hosted, with their SIL Open Font Licenses in assets/fonts/.

## Contact integration: delivery remains unverified

Read-only investigation found that WordPress admin-ajax.php returns HTTP 403 for OPTIONS both with and without an Origin header. GET without a WordPress action returns HTTP 400 and body `0`, which is consistent with the WordPress AJAX dispatcher. Those responses have no Access-Control-Allow-Origin header.

The OPTIONS rejection occurs on the original server. It does not establish whether a form POST would succeed: a browser-generated multipart FormData POST normally qualifies as a simple CORS request and does not require preflight. The separate static project has no verified same-origin WordPress integration, backend or cross-origin response permission. The precise live POST acceptance and delivery behavior cannot be established without an authorized delivery test and server configuration access. No access restrictions were bypassed and no live inquiry was submitted.

The UI therefore explicitly says online submission is unavailable. It validates the original contact fields and prepares an encoded email link for the visitor to review and send in their email app. It does not send anything automatically or claim delivery. It also links to SOCOR’s original contact page. Tests verify draft creation and that no AJAX request is sent; email delivery is not tested.

## Final audit

See audit/AUDIT.md, audit/browser-results.json and audit/screenshots/. Screenshots cover all 11 pages at 1440×1000, 834×1112 and 390×844. Additional browser checks cover 320px widths. The requested fjr-creative-ui skill remains unavailable in both the catalog and filesystem; the supplied architectural reference guided the review. Browser checks use Chromium, not physical devices or other browser engines.
