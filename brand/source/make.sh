#!/bin/zsh
# Rebuild every Week Dial deliverable from scratch: SVG masters, checks, PNG renders, the rollout set in
# out/, the manifest out/FILES.md and the sheets. Nothing in out/ is edited by hand.
# Needs: python3.14 + uv (venv is created on first run), ImageMagick 7 (magick), Google Chrome.
set -euo pipefail
cd ${0:A:h}
D=$PWD

# ---------------------------------------------------------------- venv and masters
if [[ ! -x venv/bin/python ]]; then
  uv venv -q -p 3.14 venv
  uv pip install -q -p venv/bin/python skia-pathops fonttools uharfbuzz
fi
for f in *.svg(N); do rm $f; done            # masters are generated, never edited
venv/bin/python build.py
venv/bin/python wordmark.py
venv/bin/python check.py

# ---------------------------------------------------------------- renders (headless Chrome)
for d in png out tmp; do [[ -d $d ]] && rm -r $d; done
mkdir -p png out/svg tmp
VARIANTS=(mark cards bridge webapp)
jobs=tmp/jobs.txt; : > $jobs
for v in $VARIANTS; do
  print "$v-16.svg 16 png/$v-16.png" >> $jobs
  print "$v-mono-16.svg 16 png/$v-mono-16.png" >> $jobs
  for s in 32 48; do                          # pixel-tuned tile where one exists (bridge)
    m=$v.svg; [[ -f $v-$s.svg ]] && m=$v-$s.svg
    print "$m $s png/$v-$s.png" >> $jobs
  done
  for s in 180 192 512; do print "$v.svg $s png/$v-$s.png" >> $jobs; done
  for s in 32 48; do                          # mono below 180 px: no today accent, pixel-tuned where one exists
    m=$v-mono-small.svg; [[ -f $v-mono-$s.svg ]] && m=$v-mono-$s.svg
    print "$m $s png/$v-mono-$s.png" >> $jobs
  done
  for s in 180 512; do print "$v-mono.svg $s png/$v-mono-$s.png" >> $jobs; done   # with the accent line
  print "$v-light.svg 512 png/$v-light-512.png" >> $jobs
  print "$v-maskable.svg 512 png/$v-maskable-512.png" >> $jobs
  print "$v-square.svg 180 png/$v-square-180.png" >> $jobs
  print "$v-transparent.svg 1024 png/$v-transparent-1024.png" >> $jobs
  print "$v-transparent-light.svg 1024 png/$v-transparent-light-1024.png" >> $jobs
done
print "mark-maskable.svg 500 png/mark-maskable-500.png" >> $jobs
for f in lockup*.svg; do
  read W H <<< "$(sed -n 's/.*viewBox="[-0-9.]* [-0-9.]* \([0-9.]*\) \([0-9.]*\)".*/\1 \2/p' $f | head -1)"
  W=${W%.*}; H=${H%.*}
  if [[ $f == *transparent* ]]; then
    print "$f $(( (W + 1) * 2 )) png/${f%.svg}.png $(( H * 2 ))" >> $jobs   # 2x, downsampled below
  else
    print "$f $W png/${f%.svg}.png $H" >> $jobs
  fi
done
xargs -P 8 -L 1 ./render.sh < $jobs
missing=0
while read svg w out h; do [[ -s $out ]] || { print "render failed: $out"; missing=1; }; done < $jobs
(( missing == 0 ))
venv/bin/python check_png.py png   # what Chrome draws: solid mono 16 plate, bridge deck and arch, cream gap

# ---------------------------------------------------------------- rollout set
sq() { # trimmed transparent square: in size out
  magick $1 -trim +repage -resize ${2}x${2} -background none -gravity center -extent ${2}x${2} PNG32:$3
}
logo() { # transparent lockup, shortest side (height): in height out
  magick $1 -trim +repage -resize x${2} PNG32:$3
}
for v in $VARIANTS; do
  P=""; [[ $v != mark ]] && P="$v-"
  L=lockup; [[ $v != mark ]] && L=lockup-$v
  # Home Assistant brand set: icon* for the light UI (night plate), dark_* for the dark UI (cream plate)
  sq png/$v-transparent-light-1024.png 256 out/${P}icon.png
  sq png/$v-transparent-light-1024.png 512 out/${P}icon@2x.png
  sq png/$v-transparent-1024.png 256 out/${P}dark_icon.png
  sq png/$v-transparent-1024.png 512 out/${P}dark_icon@2x.png
  logo png/$L-transparent-light.png 128 out/${P}logo.png
  logo png/$L-transparent-light.png 256 out/${P}logo@2x.png
  logo png/$L-transparent.png 128 out/${P}dark_logo.png
  logo png/$L-transparent.png 256 out/${P}dark_logo@2x.png
  # PWA / browser set
  cp $v-16.svg out/${P}favicon.svg
  magick png/$v-16.png PNG32:out/${P}favicon-16.png
  magick png/$v-32.png PNG32:out/${P}favicon-32.png
  magick png/$v-16.png png/$v-32.png png/$v-48.png out/${P}favicon.ico
  magick png/$v-square-180.png -background "#14201A" -alpha remove -alpha off PNG24:out/${P}apple-touch-icon.png
  magick png/$v-192.png PNG32:out/${P}icon-192.png
  magick png/$v-512.png PNG32:out/${P}icon-512.png
  magick png/$v-maskable-512.png -alpha off PNG24:out/${P}icon-maskable-512.png
done
magick png/mark-maskable-500.png -alpha off PNG24:out/avatar-500.png
cp *.svg out/svg/

# ---------------------------------------------------------------- verify the rollout set
fail=0
want() { # file WxH
  local got; got=$(magick identify -format '%wx%h' "$1[0]" 2>/dev/null || true)
  [[ $got == $2 ]] || { print "bad size $1: $got, want $2"; fail=1; }
}
opaque() { [[ $(magick identify -format '%[opaque]' $1) == True ]] || { print "not opaque: $1"; fail=1; }; }
clear_corner() { [[ $(magick $1 -format '%[fx:p{0,0}.a]' info:) == 0 ]] || { print "corner not transparent: $1"; fail=1; }; }
for v in $VARIANTS; do
  P=""; [[ $v != mark ]] && P="$v-"
  want out/${P}icon.png 256x256; want out/${P}icon@2x.png 512x512
  want out/${P}dark_icon.png 256x256; want out/${P}dark_icon@2x.png 512x512
  for f in icon icon@2x dark_icon dark_icon@2x logo logo@2x dark_logo dark_logo@2x; do clear_corner out/${P}$f.png; done
  for f in logo dark_logo; do
    [[ $(magick identify -format '%h' out/${P}$f.png) == 128 ]] || { print "bad height out/${P}$f.png"; fail=1; }
    [[ $(magick identify -format '%h' out/${P}$f@2x.png) == 256 ]] || { print "bad height out/${P}$f@2x.png"; fail=1; }
    (( $(magick identify -format '%w' out/${P}$f.png) > 128 )) || { print "logo not landscape: out/${P}$f.png"; fail=1; }
  done
  want out/${P}favicon-16.png 16x16; want out/${P}favicon-32.png 32x32
  [[ $(magick identify -format '%wx%h ' out/${P}favicon.ico) == "16x16 32x32 48x48 " ]] || { print "bad ico out/${P}favicon.ico"; fail=1; }
  want out/${P}apple-touch-icon.png 180x180; opaque out/${P}apple-touch-icon.png
  want out/${P}icon-192.png 192x192; want out/${P}icon-512.png 512x512
  want out/${P}icon-maskable-512.png 512x512; opaque out/${P}icon-maskable-512.png
  # maskable: everything that is not the background lies inside the 80 % safe circle (radius 204.8)
  outside=$(magick out/${P}icon-maskable-512.png -fuzz 3% -fill black -opaque "#14201A" -fill white +opaque black \
    \( -size 512x512 xc:white -fill black -draw "circle 256,256 256,51.2" \) -compose multiply -composite -format '%[fx:mean*w*h]' info:)
  (( ${outside%.*} == 0 )) || { print "maskable ink outside the safe circle: out/${P}icon-maskable-512.png ($outside px)"; fail=1; }
done
want out/avatar-500.png 500x500; opaque out/avatar-500.png
(( fail == 0 ))

# ---------------------------------------------------------------- sheets and manifest
./size-sheet.sh
./sheet.sh >/dev/null
venv/bin/python files.py
rm -r tmp
print "make.sh: ok, $(ls out | wc -l | tr -d ' ') entries in out/"
