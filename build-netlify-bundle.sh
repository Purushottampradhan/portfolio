#!/usr/bin/env bash
# Build a clean Netlify deploy folder + zip (NO .git, NO secrets).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DIST="$ROOT/dist"
ZIP="$ROOT/../business-portfolio-netlify.zip"
STAMP="$(date +%Y%m%d-%H%M%S)"
ZIP_STAMPED="$ROOT/../business-portfolio-netlify-${STAMP}.zip"

echo "==> Cleaning dist/"
rm -rf "$DIST"
mkdir -p "$DIST"

echo "==> Copying public site files only"
PUBLIC_FILES=(
  index.html
  404.html
  styles.css
  script.js
  robots.txt
  netlify.toml
  interview-prep-complete.html
  dsa-master-course.html
  Foundations_of_Artificial_Intelligence.html
  python-editor.html
  code-editor.html
  course-python-runner.css
  course-python-runner.js
  course-theme.css
  dsa-problems.js
  dsa-visual-lab.js
)

for f in "${PUBLIC_FILES[@]}"; do
  if [[ -f "$ROOT/$f" ]]; then
    cp "$ROOT/$f" "$DIST/$f"
    echo "  + $f"
  else
    echo "  ! missing: $f" >&2
  fi
done

cat > "$DIST/_headers" <<'EOF'
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
EOF

cat > "$DIST/_redirects" <<'EOF'
/.git/*  /404.html  404
/.git    /404.html  404
/.env    /404.html  404
/.env*   /404.html  404
/.gitignore  /404.html  404
EOF

if [[ -e "$DIST/.git" ]]; then
  echo "ERROR: .git found in dist — aborting" >&2
  exit 1
fi

echo "==> dist/ contents:"
find "$DIST" -type f | sed "s|$DIST/||" | sort

SIZE="$(du -sh "$DIST" | awk '{print $1}')"
echo "==> Bundle size: $SIZE"

echo "==> Creating zip for Netlify drag-and-drop"
rm -f "$ZIP"
(
  cd "$DIST"
  zip -r -q "$ZIP" .
)
cp "$ZIP" "$ZIP_STAMPED"

if unzip -l "$ZIP" | grep -E '(^|\s)\.git(/|$)' >/dev/null; then
  echo "ERROR: .git inside zip — aborting" >&2
  rm -f "$ZIP" "$ZIP_STAMPED"
  exit 1
fi

echo ""
echo "Ready to deploy (safe — no Git history)"
echo "  Folder: $DIST"
echo "  Zip:    $ZIP"
echo ""
echo "Netlify Drag & Drop:"
echo "  1. Open https://app.netlify.com/drop"
echo "  2. Upload ONLY: business-portfolio-netlify.zip"
echo "  3. Do NOT upload the business-portfolio folder (it contains .git)"
echo ""
echo "CLI:  netlify deploy --prod --dir=dist"
