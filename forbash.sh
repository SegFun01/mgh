#!/bin/bash
FILES="./input/*.mgh.json"
j=1
echo "MGH"
echo "Procesamiento de varias redes por lotes"
echo "---------------------------------------"
echo " "
for i in $FILES
do
  echo "Procesando archivo N° $j : $i"
  echo "-------------------------------------"
  python3 mgh.py $i -v
  echo "..."
  echo " "
  let "j+=1"
done
