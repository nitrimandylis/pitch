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

```html
<footer class="colophon">
  <span class="seal" aria-hidden="true"></span> built by nick trimandylis
</footer>
```

```css
.colophon { display: flex; align-items: center; gap: .6rem; opacity: .5; }
.seal {
  width: 32px; aspect-ratio: 427 / 406; background: currentColor;
  -webkit-mask: url(../assets/seal.svg) no-repeat center / contain;
  mask: url(../assets/seal.svg) no-repeat center / contain;
}
```

- It is a **mask**, not an `<img>`. That is what makes it take each pitch's own
  text colour instead of shipping a second asset per theme.
- Path is `../assets/seal.svg` from a pitch folder, `assets/seal.svg` from root.
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
