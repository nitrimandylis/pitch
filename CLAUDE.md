# CLAUDE.md — pitch

Static pitch sites, one folder each, served by GitHub Pages from `main`.

## Layout

```
index.html          root listing, one <li> per pitch under the marker comment
<slug>/index.html   the pitch site, single file, no build step
<slug>/og.png       optional 1200x1200 link-preview image
<slug>/tokens.css   optional, if hallmark emits a token file
.hallmark/log.json  hallmark's theme rotation memory, shared across all pitches
```

Live at `https://nitrimandylis.github.io/pitch/<slug>/`.

## Adding a pitch

Use the `pitch` skill (`/pitch`). It interviews, builds with hallmark, then asks
before pushing. Do not hand-write pitch sites here; the skill exists so the
grilling happens.

## Rules

- One HTML file per pitch. No frameworks, no build step, no external JS.
- Absolute URLs in `og:` meta tags, pointing at the pitch's own folder. A
  relative `og:image` does not resolve in link previews.
- Never delete or restyle an existing pitch folder while building a new one.
  `.hallmark/log.json` is append-only; it is what keeps pitches from looking
  like each other.
- No real names of friends, no school branding.
- Voice is per-pitch, decided in the interview. Nothing here is corporate.

## Deploying

`git push` to `main`. Pages picks it up in ~30s. There is no Vercel project
for this repo anymore.
