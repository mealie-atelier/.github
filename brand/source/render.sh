#!/bin/zsh
# usage: render.sh in.svg width out.png [height]
# Chrome headless sometimes hangs with tiny windows, so small icons render in a 128 px window and are cropped.
D=${0:A:h}
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p $D/tmp
P=$(mktemp -d $D/tmp/prof.XXXX)
W=$2; HH=${4:-$2}
WW=$(( W < 128 ? 128 : W )); WH=$(( HH < 128 ? 128 : HH ))
H=$D/tmp/$(basename $3 .png).$$.html
print "<html><body style='margin:0'><img src='file://${1:A}' width=$W height=$HH style='display:block'></body></html>" > $H
"$C" --headless --disable-gpu --hide-scrollbars --user-data-dir=$P --force-device-scale-factor=1 --default-background-color=00000000 --window-size=$WW,$WH --screenshot=${3:A} file://$H >/dev/null 2>&1
(( WW != W || WH != HH )) && magick ${3:A} -crop ${W}x${HH}+0+0 +repage ${3:A}
rm -r $P $H
