#!/bin/zsh
# Render the 1280x640 GitHub social previews (org, Cards, Bridge) into ../social/.
# Lockup on the Night plate colour plus a one-line English tagline. Run publish.py first.
# Needs: Google Chrome or Chromium (set CHROME to override), ImageMagick 7.
set -euo pipefail
cd ${0:A:h}
source ${0:A:h}/chrome.sh
OUT=../social; mkdir -p $OUT tmp
typeset -A TAG LOGO
TAG=(org "Your Mealie kitchen, beautifully at home in Home Assistant."
     cards "Dashboard cards for Mealie recipes, plans and shopping."
     bridge "The Home Assistant integration behind Mealie Atelier.")
LOGO=(org lockup-transparent cards lockup-cards-transparent bridge lockup-bridge-transparent)
for k in org cards bridge; do
  n=mealie-atelier-social-preview; [[ $k != org ]] && n=mealie-atelier-$k-social-preview
  svg=${LOGO[$k]}.svg
  read W H <<< "$(sed -n 's/.*viewBox="[-0-9.]* [-0-9.]* \([0-9.]*\) \([0-9.]*\)".*/\1 \2/p' $svg | head -1)"
  LW=$(( W > 1200 ? 960 : 820 ))
  cat > tmp/$k.html <<H
<html><head><style>
@font-face { font-family: B; src: url('file://${PWD}/font/BricolageGrotesque.ttf'); font-weight: 200 800; }
html,body { margin:0; width:1280px; height:640px; background:#14201A; }
body { display:flex; flex-direction:column; align-items:center; justify-content:center; gap:44px; }
img { width:${LW}px; display:block; }
p { margin:0; font: 400 34px/1.3 B, sans-serif; color:#F2E9D8; letter-spacing:-0.01em; text-align:center; }
</style></head><body><img src="file://${PWD}/$svg"><p>${TAG[$k]}</p></body></html>
H
  P=$(mktemp -d tmp/prof.XXXX)
  "$C" --headless --disable-gpu --hide-scrollbars --user-data-dir=$P --force-device-scale-factor=1 \
    --window-size=1280,640 --screenshot=${PWD}/tmp/$k.png file://${PWD}/tmp/$k.html >/dev/null 2>&1
  rm -r $P
  magick tmp/$k.png -alpha off -strip PNG24:$OUT/$n.png
  magick $OUT/$n.png -quality 88 -strip $OUT/$n.jpg
done
rm -r tmp
