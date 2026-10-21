# Deploy this portfolio to Netlify (safe — no Git history)

## Why not upload the whole folder?

Your `business-portfolio` folder contains a `.git` directory. If you drag that
folder (or a zip that includes `.git`) to Netlify, visitors or scanners can
sometimes discover repo metadata, old commits, or local paths. That is unsafe.

**Always deploy the clean `dist/` folder or `business-portfolio-netlify.zip`.**

## One-command bundle

```bash
cd business-portfolio
chmod +x build-netlify-bundle.sh
./build-netlify-bundle.sh
```

This creates:

| Output | Purpose |
|--------|---------|
| `dist/` | Clean site root (upload this, or set as Netlify publish dir) |
| `../business-portfolio-netlify.zip` | Drag-and-drop zip for Netlify Drop |

The script **never** copies `.git`, `.env`, or `node_modules`.

## Deploy options

### A) Netlify Drag & Drop (simplest)

1. Run `./build-netlify-bundle.sh`
2. Open [https://app.netlify.com/drop](https://app.netlify.com/drop)
3. Upload **`business-portfolio-netlify.zip`** (from the `learnings/` folder)
4. Netlify gives you a URL like `https://random-name.netlify.app`

### B) Netlify CLI

```bash
npm i -g netlify-cli
cd business-portfolio
./build-netlify-bundle.sh
netlify login
netlify deploy --prod --dir=dist
```

### C) Git-connected site (recommended long-term)

1. Create a **new empty public/private repo** with **only** the contents of `dist/`
   (or keep source privately and publish `dist` via CI).
2. In Netlify: New site → Import from Git → set publish directory to `/` if the
   repo is only the site files.
3. Never push `.git` from this machine into the deploy artifact — Git hosts the
   repo; Netlify builds from it without exposing `.git` on the CDN.

## Security included

- `netlify.toml` + `_headers`: frame deny, nosniff, referrer policy
- `_redirects`: `/.git/*` and `/.env*` → 404
- Custom `404.html`

## Checklist before each deploy

- [ ] Ran `./build-netlify-bundle.sh`
- [ ] Confirmed `dist/` has **no** `.git`
- [ ] Uploading **zip** or **dist/** — not the parent folder with `.git`
- [ ] Opened the live site and checked Home → Interview prep → Back works
