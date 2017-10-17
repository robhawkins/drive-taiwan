#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
OUT="$DIR"/output-html
mkdir -p "$OUT"

nprocs=1
OS=$(uname -s)

if [[ "$OS" == "Linux" ]] ; then
  nprocs=$(grep -c ^processor /proc/cpuinfo)
elif [[ "$OS" == "Darwin" ]] ; then
  nprocs=$(sysctl -n hw.ncpu)
fi

for l in chinese english; do
  for v in moto car; do
    echo $l $v
  done
done | xargs -n 2 -P4 sh -c "python3 -B \"$DIR\"/produceHTML.py -l \$1 -v \$2 " argv0
