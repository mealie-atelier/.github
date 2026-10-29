# Sourced by render.sh and social.sh: sets $C to a Chrome or Chromium binary.
# Order: $CHROME, the macOS app, then google-chrome, chromium or chromium-browser on PATH.
if [[ -n ${CHROME:-} ]]; then
  C=$CHROME
elif [[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
  C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else
  C=$(whence -p google-chrome chromium chromium-browser 2>/dev/null | head -1 || true)
fi
if [[ -z $C || ! -x $C ]]; then
  print -u2 "No Chrome found. Install Google Chrome or Chromium, or set CHROME=/path/to/chrome."
  exit 1
fi
