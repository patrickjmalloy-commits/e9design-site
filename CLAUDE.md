# E9 Design site

Static HTML site for E9 Design (Emergency Nine Design), custom golf simulators,
Mason OH. Hosted on Netlify. `staging` deploys to the Netlify staging site;
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

- Five public pages: Home, Simulators, How It Works, Showroom, Contact. Plus
  /thank-you/ (form landing) and 404, both noindex. Keep the site small.
- Same menu on every page; one phone number, (513) 886-6654.
- No email address on the site: E9 has no working mailbox yet (Nov 2026).
  Visitors use the contact form. Add an address only once it is confirmed to
  receive mail.
- One palette, defined in css/site.css: pine #12343A, turf #2F6B3A, oak #C08A4E,
  cream #F6F3EC, ink #172426. No inline colours outside that set.
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
