# CLAUDE.md — flight-001 pitch site

## What this project is

A one-page, mobile-first pitch website used to recruit 2-3 friends for a
final-year hackathon season. Currently live at https://flight-001.vercel.app
on the Vercel project `flight-001` (team: nitrimandylis-projects), deployed
as a static site with no build step.

Files:
- `index.html` — the entire site (HTML, CSS, JS in one file)
- `og.png` — 1200x630 Open Graph image, referenced by absolute URL in the
  meta tags

## The task

Repitch the site. It currently sells ONE event (NASA Space Apps, Nov 14-15).
The audience read it and is lukewarm on the NASA hackathon specifically, but
they're in. The site should now sell the SEASON, with NASA as merely the
first stop.

The season, factually:
- 3-4 online hackathon sprints between September 2026 and February 2027
- Hard stop in February for IB exam prep (exams May 2027)
- Sprint 1: NASA Space Apps Challenge, Nov 14-15, 2026 (free, online,
  teams up to 6, no coding required for most roles)
- Sprints 2-4: picked from Hack Club's online calendar and Devpost as
  autumn listings publish; criteria: high-school eligible, EU-timezone
  friendly or async, non-entrepreneurship
- Success metric: 3-4 shipped demos, placements are upside, morale matters
- Roles: Build is taken (Nick). Design, Pitch, Research are open
- A reusable Next.js base gets built in August so comp weekends are
  design, pitch and demo work, not plumbing

## Content changes

1. Reframe the hero around the season, not NASA. "One weekend" was the
   original hook; the new hook is the arc: 4 flights, one crew, done
   before exams. Keep it short and confident.
2. Demote NASA to "Flight 001" — one row in a flight schedule, not the
   headline. Add a flight schedule section: 001 NASA Space Apps (Nov
   14-15, confirmed), 002-004 marked TBD / announced monthly. TBD rows
   should look intentional, like a launch manifest, not like missing
   content.
3. Keep the crew manifest section as is (roles and open/locked tags).
4. Keep or lightly adapt the objections section. Add one new objection:
   "Why NASA? Sounds nerdy." Answer honestly: it's the biggest, it's
   free, and it's only stop one — nobody is marrying the space theme.
5. Update the topbar "FLIGHT 001 / 04" to something season-level, e.g.
   "SEASON 26-27" left, "4 FLIGHTS" right, or similar.
6. Update <title>, meta description, og:title, og:description to match
   the season framing.
7. The CTA stays a clipboard-copy button. Update the copied string to a
   season-level reply (e.g. "in for the season").

## Voice

- Deadpan, ironic, confident. Short sentences. No exclamation marks,
  no corporate hype words (journey, unlock, empower, elevate).
- No em dashes anywhere in copy. Use periods and commas.
- Audience is 17-18 year old friends, not admissions officers. If a
  line would work in a LinkedIn post, cut it.
- Do not oversell NASA. The honest angle is: forced deadlines, shipped
  projects, all-nighters with friends, done before exams.

## Design system (do not change)

- Single file. No frameworks, no build step, no external JS.
- Palette: paper #FAFAF7, ink #14171C, red #E4321F, blue #0B3D91,
  rule #D8D6CF. Vars already defined in :root.
- Type: Archivo Black (display), Archivo (body), IBM Plex Mono
  (labels/data). Loaded from Google Fonts.
- Aesthetic: 1970s NASA graphics-manual / mission-briefing document.
  Heavy 3px ink rules, mono uppercase labels, red used sparingly.
- Mobile-first, max-width 640px, one column. Test at 380px width.
- Keep prefers-reduced-motion handling and the button focus-visible
  outline.

## OG image

`og.png` is generated, not designed by hand. If the headline changes,
regenerate it to match: 1200x630, same palette, topbar + eyebrow +
big Archivo Black headline + facts strip. Fonts can be fetched from
raw.githubusercontent.com/google/fonts (ofl/archivoblack,
ofl/ibmplexmono). A Pillow script produced the current one; recreate
in the same style. Keep it under ~100KB.

## Deploying

Deploy with the Vercel MCP tool `deploy_to_vercel`:
- name: `flight-001`
- target: `production`
- files: BOTH `index.html` (utf-8) and `og.png` (base64). A deploy
  replaces the whole file tree, so omitting og.png takes the OG image
  down and breaks link previews.
- Verify with `get_deployment` until state is READY, then sanity-check
  https://flight-001.vercel.app and the og:image URL.

## Out of scope

- No new pages, no framework migration, no analytics, no forms.
- Do not add real names of the friends anywhere.
- Do not add school branding; this is explicitly not a school thing.
