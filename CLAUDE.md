# CLAUDE.md — pitch

Static pitch sites, one folder each, served by GitHub Pages from `main`.

## Layout

```
index.html          root listing, one <li> per pitch under the marker comment
assets/seal.svg     the seal mark, shared by every pitch, see Colophon below
<slug>/index.html   the pitch site, single file, no build step
<slug>/og.png       1200x1200 link-preview image, generated on every build
<slug>/tokens.css   optional, if hallmark emits a token file
.hallmark/log.json  hallmark's theme rotation memory, shared across all pitches
```

Live at `https://nitrimandylis.github.io/pitch/<slug>/`.

## Adding a pitch

Use the `pitch` skill (`/pitch`). It interviews, builds with hallmark, then asks
before pushing. Do not hand-write pitch sites here; the skill exists so the
grilling happens.

## Colophon

Every pitch ends with the seal mark and a line of attribution. It is the only
thing shared across pitches, so it is the one signal that they come from the
same person.

Paste the whole contents of `assets/seal.svg` inline, adding
`class="seal" aria-hidden="true"` to its opening `<svg>` tag:

```html
<footer class="colophon">
  <svg class="seal" aria-hidden="true" ...>…</svg> built by nick trimandylis
</footer>
```

```css
.colophon { display: flex; align-items: center; gap: .6rem; opacity: .5; }
.seal { width: 32px; height: auto; flex: none; }
```

- **Inline, not `<img>` and not `mask-image`.** Inline is the only form where
  `fill="currentColor"` picks up the pitch's own text colour. An external SVG
  used as a CSS mask silently fails over `file://`, which is exactly how every
  pitch gets reviewed before it ships, so it would look fine live and broken
  in review.
- `assets/seal.svg` is the source of truth. Copy from it, never hand-edit the
  copy pasted into a page.
- Keep it at 28-40px. It is traced line art and turns to mush below ~24px.
- Do not restyle it per pitch beyond size and opacity. Sameness is the point.

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
