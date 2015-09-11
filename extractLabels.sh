#!/bin/bash

ankiExport="$1"

if [[ ! -f "$ankiExport" ]] ; then
  echo ERROR: file not found: "$ankiExport"
  exit 1
fi
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

TARGET="$DIR"/input/difficulty-labels.txt
TMP="$TARGET".tmp

egrep '\t(easy|medium|hard|impossible)\t' "$ankiExport" | cut -d"$(printf '\t')" -f1 -f9 | tr '\t' ' '| sed 's/^[a-z]*/any/' > "$TMP"

if [[ -f "$TARGET" ]] ; then
  TMPNEW="$TMP".new
  sort -u "$TARGET" "$TMP" > "$TMPNEW"
  mv "$TMPNEW" "$TARGET"
  rm "$TMP"
else
  mv "$TMP" "$TARGET"
fi

echo $TARGET

matches=$(cat "$TARGET" | awk '{print $1}' | sort | uniq -c | grep -v ' 1 ')
res=$?
matchesCut=$(printf "$matches\n" | awk '{print $2}')
if [[ $res == 0 ]] ; then
  for r in $matchesCut; do
    grep $r "$TARGET"
  done
  echo ERROR: Conflicting entries found, please resolve
fi
