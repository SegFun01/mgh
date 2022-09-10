#!/bin/bash
FILES="./input/*.mgh.json"
for i in $FILES
do
  python3 mgh.py $i -v
done
