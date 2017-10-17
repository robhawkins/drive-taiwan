#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

"$DIR"/genAllCSV.sh

"$DIR"/genAllHTML.sh
