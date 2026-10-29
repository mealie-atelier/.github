#!/bin/zsh
# Compose out/size-sheet.png from png/ renders: mark, mono and the family at 16, 32, 48, 180 and 512 px,
# all 1:1, on cream, white, black and a dark UI grey. Mono is black on light grounds, white on dark ones.
# Called by make.sh.
set -euo pipefail
cd ${0:A:h}
T=tmp/size; mkdir -p $T
F=font/BricolageGrotesque.ttf
SIZES=(16 32 48 180 512)
BGS=("#F2E9D8" "#FFFFFF" "#000000" "#202124")
NAMES=("cream #F2E9D8" "white" "black" "dark #202124")
ROWS=(mark mark-mono cards cards-mono bridge bridge-mono webapp webapp-mono)
PAD=20; RH=$(( 512 + 2 * PAD ))
lab() { magick -background none -fill "$3" -font $F -pointsize ${4:-22} label:"$1" $2; }

blocks=()
for i in {1..4}; do
  bg=${BGS[$i]}
  ink="#14201A"; [[ $bg == "#000000" || $bg == "#202124" ]] && ink="#F2E9D8"
  rows=()
  for r in $ROWS; do
    cells=()
    for s in $SIZES; do
      if [[ $r == *-mono ]]; then
        v=${r%-mono}
        src=png/$v-mono-$s.png
        neg=(); [[ $ink != "#14201A" ]] && neg=(-channel RGB -negate +channel)
        magick $src $neg -background "$bg" -gravity center -extent $(( s + 2 * PAD ))x$RH $T/c-$i-$r-$s.png
      else
        magick png/$r-$s.png -background "$bg" -gravity center -extent $(( s + 2 * PAD ))x$RH $T/c-$i-$r-$s.png
      fi
      cells+=($T/c-$i-$r-$s.png)
    done
    magick $cells +append $T/r-$i-$r.png
    rows+=($T/r-$i-$r.png)
  done
  # header: background name and the size of every column
  W=$(magick identify -format %w $rows[1])
  heads=()
  for s in $SIZES; do
    lab "$s" $T/h-$s.png "$ink"
    magick $T/h-$s.png -background "$bg" -gravity center -extent $(( s + 2 * PAD ))x36 $T/hh-$i-$s.png
    heads+=($T/hh-$i-$s.png)
  done
  magick $heads +append $T/heads-$i.png
  lab "${NAMES[$i]}" $T/n-$i.png "$ink" 28
  magick $T/n-$i.png -background "$bg" -gravity center -extent ${W}x56 $T/nn-$i.png
  magick $T/nn-$i.png $T/heads-$i.png $rows -append $T/b-$i.png
  blocks+=($T/b-$i.png)
done

# row labels on the left
labels=()
magick -size 200x92 xc:"#E8E2D6" $T/l-head.png
for r in $ROWS; do
  n=${r/-mono/ mono}; n=${n/mark/Mealie Atelier}; n=${n/webapp/web app}; n=${n/cards/Cards}; n=${n/bridge/Bridge}
  lab "$n" $T/l.png "#14201A"
  magick $T/l.png -background "#E8E2D6" -gravity center -extent 200x$RH $T/l-$r.png
  labels+=($T/l-$r.png)
done
magick $T/l-head.png $labels -append $T/labels.png
lab "Week Dial  ·  size sheet, every image 1:1 (16, 32, 48, 180, 512 px)  ·  mono: black on light, white on dark" $T/title.png "#14201A" 26
magick $T/labels.png $blocks -background "#E8E2D6" +append $T/grid.png
magick $T/title.png $T/grid.png -background "#E8E2D6" -gravity northwest -splice 0x24 -append -bordercolor "#E8E2D6" -border 32 +repage out/size-sheet.png
