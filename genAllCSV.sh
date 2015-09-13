#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
OUT="$DIR"/output
mkdir -p "$OUT"

nprocs=1
OS=$(uname -s)

if [[ "$OS" == "Linux" ]] ; then
  nprocs=$(grep -c ^processor /proc/cpuinfo)
elif [[ "$OS" == "Darwin" ]] ; then
  nprocs=$(sysctl -n hw.ncpu)
fi

find "$DIR"/input/pdf/ -type f -name '*.pdf' | xargs -P${nprocs} -I, python3 convert.py -f , -w "$OUT" "$@"

