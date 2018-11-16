#!/bin/bash

while getopts i:o: opts; do
   case ${opts} in
      i) IN_FILE=${OPTARG} ;;
      o) OUT_FILE=${OPTARG} ;;
   esac
done

if [ -z $IN_FILE ] || [ -z $OUT_FILE ] ; then
  echo "usage:"
  echo "  montag.sh -i <IN_FILE> -o <OUT_FILE>"
  exit 1
elif [ ! -f $IN_FILE ]; then
  echo "usage:"
  echo "  montag.sh -i <IN_FILE> -o <OUT_FILE>"
  echo ""
  echo "$IN_FILE does not exist!"
  exit 1
fi

TEMP_DIR=$(mktemp -d -t tmp.XXXXXXXXXX)

function finish {
  rm -rf "$TEMP_DIR"
}

trap finish EXIT

IN_BASENAME="$(basename "$IN_FILE")"
OUT_BASENAME="$(basename "$OUT_FILE")"

cp "$IN_FILE" "$TEMP_DIR/"

docker run --rm -t \
  -v "$TEMP_DIR:/data:rw" \
  montag:latest -i "/data/$IN_BASENAME" -o "/data/$OUT_BASENAME"

cp "$TEMP_DIR/OUT_BASENAME" "$OUT_FILE"

echo "$OUT_FILE"
