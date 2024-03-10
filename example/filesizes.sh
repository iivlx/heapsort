#!/bin/bash

file_sizes=""

for file in *; do
    if [ -f "$file" ]; then
        file_sizes+=$(stat -c%s "$file")" "
    fi
done

echo "${file_sizes% }" > filesizes.dat
