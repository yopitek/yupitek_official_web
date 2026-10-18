#!/bin/bash
for locale in zh-tw zh-cn en ja ar es pt ru de fr; do
  for file in content/$locale/products/sierra/_index.md; do
    echo "Checking $file"
    grep "image=" "$file" | while read -r line; do
      img=$(echo "$line" | grep -oP 'image="\K[^"]+')
      if [ ! -f "static$img" ]; then
        echo "MISSING: $img in $file"
      fi
    done
  done
done
