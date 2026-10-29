#!/bin/zsh
# Compose out/overview-sheet.png (maskable crops, GitHub crops, lockups) from png/ renders. Called by make.sh.
cd ${0:A:h}
T=tmp/sheet; mkdir -p $T
F=font/BricolageGrotesque.ttf
BG="#E8E2D6"
lab() { magick -background none -fill "#14201A" -font $F -pointsize 22 label:"$1" $2; }
pad() { magick $1 -background none -gravity center -extent $(( $(magick identify -format %w $1) + $2 ))x$(( $(magick identify -format %h $1) + $2 )) $3; }
cell() { # image label out [bg]
  magick $1 -background "${4:-none}" -gravity center -extent $(( $(magick identify -format %w $1) + 24 ))x$(( $(magick identify -format %h $1) + 24 )) $T/c.png
  lab "$2" $T/l.png
  magick $T/c.png $T/l.png -background none -gravity center -append $T/c2.png
  W=$(magick identify -format %w $T/c2.png); (( W < 150 )) && W=150
  magick $T/c2.png -background none -gravity south -extent $(( W + 20 ))x$(magick identify -format %h $T/c2.png) $3
}
x8() { magick $1 -filter point -resize 800% $2; }
# masks
magick -size 512x512 xc:none -fill white -draw "circle 256,256 256,0" $T/circle.png
magick -size 512x512 xc:none -fill white -draw "roundrectangle 0,0 511,511 150,150" $T/squircle.png
circ() { magick $1 -resize 512x512 $T/circle.png -compose DstIn -composite $2; }
squi() { magick $1 $T/squircle.png -compose DstIn -composite $2; }

# row 1: small sizes 1:1 on light and dark, plus 8x
i=0; for s in 16 32 48; do
  src=png/mark-$s.png
  cell $src "$s px 1:1" $T/a$s.png "#FFFFFF"
  cell $src "$s px on dark" $T/b$s.png "#0B0F0D"
  x8 $src $T/x$s.png; cell $T/x$s.png "$s px x8" $T/z$s.png
done
magick png/mark-mono-16.png -channel RGB -negate +channel $T/mono16w.png
cell png/mark-mono-16.png "mono 16 on white" $T/m0.png "#FFFFFF"
cell $T/mono16w.png "mono 16 on black" $T/m00.png "#000000"
magick png/mark-mono-32.png -channel RGB -negate +channel $T/mono32w.png
cell png/mark-mono-32.png "mono 32 on white" $T/m1.png "#FFFFFF"
cell $T/mono32w.png "mono 32 on black" $T/m2.png "#000000"
magick $T/a16.png $T/b16.png $T/a32.png $T/b32.png $T/a48.png $T/b48.png $T/m0.png $T/m00.png $T/m1.png $T/m2.png $T/z16.png $T/z32.png $T/z48.png -background none -gravity south +append $T/row1.png

# row 2: 180, 512, maskable circle/squircle, github crop
cell png/mark-180.png "180 apple touch" $T/r180.png
cell png/mark-512.png "512 PWA" $T/r512.png
circ png/mark-maskable-512.png $T/mc.png; cell $T/mc.png "maskable, circle" $T/rmc.png
squi png/mark-maskable-512.png $T/ms.png; cell $T/ms.png "maskable, squircle" $T/rms.png
magick png/mark-maskable-512.png -fill none -stroke "#D9572B" -strokewidth 2 -draw "circle 256,256 256,51" $T/msafe.png; cell $T/msafe.png "maskable + 80% safe circle" $T/rsafe.png
magick $T/r180.png $T/r512.png $T/rmc.png $T/rms.png $T/rsafe.png -background none -gravity south +append $T/row2.png

# row 3: github crop, mono 512 white/black, light tile
circ png/mark-512.png $T/gh1.png; magick $T/gh1.png -resize 256x256 $T/gh1s.png; cell $T/gh1s.png "GitHub crop (tile)" $T/g1.png "#FFFFFF"
circ png/mark-maskable-512.png $T/gh2.png; magick $T/gh2.png -resize 256x256 $T/gh2s.png; cell $T/gh2s.png "GitHub crop (full bleed)" $T/g2.png "#0D1117"
magick png/mark-mono-512.png -resize 256x256 $T/mo.png; cell $T/mo.png "mono on white" $T/mo1.png "#FFFFFF"
magick $T/mo.png -channel RGB -negate +channel $T/mow.png; cell $T/mow.png "mono on black" $T/mo2.png "#000000"
magick png/mark-transparent-light-1024.png -resize 256x256 $T/bare1.png; cell $T/bare1.png "bare plate on white" $T/ba1.png "#FFFFFF"
magick png/mark-transparent-1024.png -resize 256x256 $T/bare2.png; cell $T/bare2.png "bare plate on #111613" $T/ba2.png "#111613"
magick $T/g1.png $T/g2.png $T/mo1.png $T/mo2.png $T/ba1.png $T/ba2.png -background none -gravity south +append $T/row3.png

# row 4: family dark and light at 192, plus 32 and 16 (x1 and x4)
for v in mark cards bridge webapp; do
  n=$v; [[ $v == mark ]] && n="Mealie Atelier"; [[ $v == webapp ]] && n="web app"; [[ $v == cards ]] && n="Cards"; [[ $v == bridge ]] && n="Bridge"
  magick png/$v-512.png -resize 192x192 $T/fd-$v.png; cell $T/fd-$v.png "$n" $T/fdc-$v.png
  magick png/$v-light-512.png -resize 192x192 $T/fl-$v.png; cell $T/fl-$v.png "$n, light" $T/flc-$v.png
  magick png/$v-16.png -filter point -resize 400% $T/f16-$v.png
done
magick $T/fdc-{mark,cards,bridge,webapp}.png $T/flc-{mark,cards,bridge,webapp}.png -background none -gravity south +append $T/row4a.png
magick png/mark-32.png png/cards-32.png png/bridge-32.png png/webapp-32.png -background none -gravity west -splice 12x0 +append $T/f32.png; cell $T/f32.png "family 32 px 1:1" $T/f32c.png "#FFFFFF"
magick png/mark-16.png png/cards-16.png png/bridge-16.png png/webapp-16.png -background none -gravity west -splice 8x0 +append $T/f16.png; cell $T/f16.png "family 16 px 1:1" $T/f16c.png "#FFFFFF"
magick $T/f16-{mark,cards,bridge,webapp}.png -background none -gravity west -splice 16x0 +append $T/f16x.png; cell $T/f16x.png "family 16 px x4" $T/f16xc.png
magick png/mark-mono-16.png png/cards-mono-16.png png/bridge-mono-16.png png/webapp-mono-16.png -background none -gravity west -splice 8x0 +append $T/fm16.png; cell $T/fm16.png "family mono 16 px 1:1" $T/fm16c.png "#FFFFFF"
for v in mark cards bridge webapp; do magick -size 16x16 xc:white png/$v-mono-16.png -composite -filter point -resize 400% $T/fm16-$v.png; done
magick $T/fm16-{mark,cards,bridge,webapp}.png -background none -gravity west -splice 16x0 +append $T/fm16x.png; cell $T/fm16x.png "family mono 16 px x4" $T/fm16xc.png
magick $T/f16c.png $T/f32c.png $T/fm16c.png $T/f16xc.png $T/fm16xc.png -background none -gravity south +append $T/row4b.png

# row 5: lockups
magick png/lockup.png -resize 50% $T/lk1.png; magick png/lockup-light.png -resize 50% $T/lk2.png
magick $T/lk1.png $T/lk2.png -background none -splice 24x0 +append $T/row5a.png
magick png/lockup-cards.png png/lockup-bridge.png png/lockup-webapp.png -resize 40% -background none -splice 24x0 +append $T/row5b.png
lab "Week Dial (week plate)  ·  wordmark: Bricolage Grotesque 520/380, wdth 100, opsz 96 (SIL OFL)" $T/title.png

magick $T/title.png $T/row1.png $T/row2.png $T/row3.png $T/row4a.png $T/row4b.png $T/row5a.png $T/row5b.png -background "$BG" -gravity northwest -splice 0x28 -append +repage -bordercolor "$BG" -border 32 +repage out/overview-sheet.png
magick identify out/overview-sheet.png
