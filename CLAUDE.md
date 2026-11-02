# Emergency Nine Design site

Static HTML site for Emergency Nine Design (E9), Mason OH. **What E9 does:** it
helps people design and build golf entertainment spaces (home golf rooms and
commercial golf spaces). Simulators are part of those builds; E9 is NOT a
"golf simulator company", so don't describe it that way. Hosted on Netlify. `staging` deploys to the Netlify staging site;
`main` is production (e9design.net) and only moves when Patrick approves the
"Promote staging to production" workflow. Never push or merge to `main` directly.

## Repo notes are never published

Netlify serves file names in any letter case, so the build command in
netlify.toml deletes CLAUDE.md, README.md and SETUP.md from each deploy. Any
new .md file at the root must be added to that command (the site rules check).

## Before pushing to staging

    python3 .github/scripts/site_rules.py

Fix everything it reports. The release workflow runs the same check.

## Site rules (enforced by the script above)

- Five public pages: Home, Services, Process, Showroom, Contact. Plus
  /thank-you/ (form landing) and 404, both noindex. Keep the site small.
- Same menu on every page; one phone number, (513) 886-6654.
- No email address on the site: E9 has no working mailbox yet (Nov 2026).
  Visitors use the contact form. Add an address only once it is confirmed to
  receive mail.
- One palette, defined in css/site.css: black #0E0E0E, ink #141414, ivory
  #F7F3EC, red #C8102E (buttons, accent lines), red-light #FF6B6B (small red
  text on dark), red-dark #B30E29 (small red text on light). Red stays small:
  never large red areas. Headings Playfair Display with one italic accent
  phrase per heading; body Inter. Both self-hosted in /fonts (OFL, see
  fonts/README.txt). Serif numbers must use lining figures.
- Header shows the name "EMERGENCY NINE DESIGN" (no logo). The full logo
  appears once, in the home-page hero. The home hero follows the Revelance
  hero style: full-screen real showroom photo (showroom-wide), dark gradient,
  grain, centered serif headline, facts row. Inner pages use a photo header
  band; don't repeat the same photo twice on one page.
- List markers (.checks) are pixel-positioned so they render identically;
  keep line-height in px if you change them.
- Tab icon = the logo mark
  (favicon.svg / .ico / apple-touch-icon; bump ?v= in the <head> links when it
  changes).
- **American English** everywhere (color, center, practice, gray). The site
  rules flag common British spellings.
- Every page: one h1, title, meta description, canonical, viewport.
- Every image has alt text and width/height. Photos ship as .jpg plus -sm/-lg .webp.
- No breadcrumbs. Every opened tag closes in order. JSON-LD must parse.
- Every page with a phone or email link carries the `e9-contact-clicks` tracker.
  If GA4 is added, every page that loads it must also run gtag('config', ...).

## Honesty rules for content

E9 is a new business. Do not claim past installs, client counts, reviews,
"most popular", response times, or staff (e.g. instructors) that do not exist.

Images:
- E9 mainly installs overhead launch monitors (ProTee VX). Photos must not show
  floor-standing launch monitors.
- images/ai-*.{jpg,webp} are AI-generated (Figma AI image, Nov 2026). They are
  not E9 installs. Room photos (ai-basement, ai-garage, ai-commercial,
  ai-home-swing) are shown as examples of what E9 designs; where a room photo
  sits beside copy about E9's work, it keeps the "Design concept" tag. Never
  caption an AI image as a client project or as E9 staff.
- showroom-*, simulator-bay are real photos of the Emergency 9 room in Mason.
- No images copied from other sites. Replace AI images with real install photos
  as projects are completed.
