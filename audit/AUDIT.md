# Final SOCOR audit — November 11, 2026 (Asia/Singapore)

## Scope and design review

Preserved the six primary pages and five service detail pages. No framework replacement, runtime dependency addition, database/backend work, deployment or modification to the live SOCOR website.

The supplied architectural reference guided the review: monumental wordmark, cinematic photograph, compact navigation, restrained translucent information panel, fine rules and editorial contrast. The requested `$fjr-creative-ui` skill was not found in the available cloud catalog or filesystem, so it could not be applied.

### Targeted improvements

- Self-hosted Barlow Condensed and DM Sans with licenses. Browser screenshots exposed third-party font failures that changed the hero’s proportions and caused clipping.
- Removed the artificial triangular road mask that cut out the center of SOCOR and obscured its supporting line. Kept the complete wordmark, separate italic supporting line, original photograph and restrained atmospheric layering. The hero uses graphic/photo depth rather than a fabricated foreground object cutout.
- Balanced mobile hero spacing and tablet CTA placement. Fixed the Projects headline overflow at 390px and below.
- Kept distinct primary compositions: editorial company history, staggered photographic portfolio, indexed services, technical inventory and an inquiry-focused contact layout. Alternated service image/text order, varied detail-page arrangements and replaced repeated detail headings with service-specific copy. Reworked the homepage quality section into an asymmetric editorial composition.
- Added intrinsic image dimensions, eager loading for meaningful first images, hero/font preloads and local font delivery.
- Corrected sticky-header layout behavior. Improved mobile menu dismissal, keyboard access, gallery Escape/focus restoration and narrow inventory keyboard scrolling.
- Added one-time image reveals; content remains visible without JavaScript. Reduced-motion disables reveals, entrance animation and smooth scrolling, including a preference change during the session.
- Replaced the unverified AJAX send action with an explicitly unsent email-preparation flow. Added a link to the original SOCOR contact page.

## Verification

Browser viewport matrix: all 11 pages at 1440×1000, 834×1112 and 390×844, with screenshots in screenshots/. Additional 320px checks cover all 11 routes. The 320px equipment table intentionally scrolls inside a labeled, keyboard-focusable region.

The browser regression suite covers direct URLs, refreshes, active navigation, 16 unique internal destinations, five legacy redirects, back/forward navigation, mobile menu keyboard interaction, sticky headers, project filters, gallery focus return, all 42 equipment rows/search/no-results/reset, reduced motion, skip navigation and contact validation/draft handling. No live inquiry is sent by the tests.

The static suite checks unique metadata, one H1 per page, heading order, duplicate IDs, local assets, link fragments and image alternatives/dimensions. JavaScript syntax checking and the static build are run separately. Build output excludes audit tooling and evidence.

Final result: the browser interaction suite passed. axe-core reported zero WCAG A/AA violations across all 11 pages at desktop, tablet and mobile sizes (33 scans). JavaScript syntax, static checks and build also passed. See browser-results.json for the detailed interaction result. Automated accessibility checks supplement visual and keyboard review; they do not certify conformance. Image-overlay text was also reviewed in screenshots.

## Contact endpoint investigation

Read-only requests to the original admin-ajax.php endpoint:

| Request | Response | Observation |
| --- | --- | --- |
| GET, no action | 400, body `0` | Consistent with WordPress AJAX dispatch without a valid action |
| GET with localhost Origin | 400, body `0` | No Access-Control-Allow-Origin header |
| OPTIONS, no Origin | 403 | Rejection occurs on the original server |
| OPTIONS with localhost Origin / POST preflight request header | 403 | Same restriction; no CORS allow header |

The 403 is the original server’s OPTIONS behavior, independent of redesigned frontend rendering. Its precise server rule is not visible. It is not proof that a simple multipart POST would be rejected: the former FormData fetch would normally avoid preflight. The local recreation lacks a verified integration and permission to read a cross-origin success response. No form POST was made and no restriction was bypassed.

Outstanding: an authorized same-origin backend integration or server-approved cross-origin integration plus a controlled delivery test. The current form prepares a draft only and says nothing has been sent. This is a verified local handoff, not verified inquiry delivery.

## Remaining limits

- Chromium viewport testing; no Safari/Firefox or physical device verification.
- Current credentials, equipment availability and detailed project scopes/dates remain unverified; no new claims were added.
- Some authentic project photographs are archival and have limited source resolution.
- The unavailable fjr-creative-ui skill could not be used.

## Files changed

- All 11 page HTML files: local font preload, metadata/image improvements; homepage composition; contact disclosure/email handoff; equipment region/caption; gallery accessible name and detail-page active-location semantics.
- 404.html: shared local font setup.
- style.css: local fonts, hero corrections, editorial layouts, responsive fixes, contrast, motion and focus improvements.
- app.js: menu/gallery behavior, draft-only contact flow, sticky header and optional image reveals.
- assets/fonts/: local fonts and licenses.
- serve.py: clean GET/HEAD routes and custom 404 response.
- build.py: restrict packaging to public site assets.
- verify.py, browser_verify.py and package.json: static and browser audit commands.
- README.md and audit/: final documentation, test-only axe-core and evidence.
- dist/: regenerated static production files.
