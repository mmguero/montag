#!/usr/bin/env bash

export MONTAG_IMAGE="${MONTAG_DOCKER_IMAGE:-ghcr.io/mmguero/montag:latest}"

ENCODING="utf-8"
while getopts i:o:s:e: opts; do
   case ${opts} in
      i) IN_FILE=${OPTARG} ;;
      o) OUT_FILE=${OPTARG} ;;
      s) SWEARS_FILE=${OPTARG} ;;
      e) ENCODING=${OPTARG} ;;
   esac
done

if [[ -z $IN_FILE || -z $OUT_FILE ]] ; then
  echo "usage:"
  echo "  montag-docker.sh -i <IN_FILE> -o <OUT_FILE> [-s <PROFANITY_FILE> -e <ENCODING>]"
  exit 1
elif [[ ! -f "$IN_FILE" ]]; then
  echo "usage:"
  echo "  montag-docker.sh -i <IN_FILE> -o <OUT_FILE> [-s <PROFANITY_FILE> -e <ENCODING>]"
  echo ""
  echo "$IN_FILE does not exist!"
  exit 1
fi

TEMP_DIR=$(mktemp -d -t montag.XXXXXXXXXX)

function finish {
  rm -rf "$TEMP_DIR"
}
trap finish EXIT

IN_BASENAME="$(basename "$IN_FILE")"
OUT_BASENAME="$(basename "$OUT_FILE")"

cp "$IN_FILE" "$TEMP_DIR/"

if [[ -n "$SWEARS_FILE" && -f "$SWEARS_FILE" ]] ; then
  cp "$SWEARS_FILE" "$TEMP_DIR/swears.txt"
  SWEARS_MAP="-v "$TEMP_DIR/swears.txt:/usr/local/bin/swears.txt:ro""
else
  SWEARS_MAP=""
fi

docker run --rm -t \
  -v "$TEMP_DIR:/data:rw" $SWEARS_MAP \
  "$MONTAG_IMAGE" -i "/data/$IN_BASENAME" -o "/data/$OUT_BASENAME" -e "$ENCODING"

cp "$TEMP_DIR/$OUT_BASENAME" "$OUT_FILE"

echo "$OUT_FILE"
