#!/bin/zsh
source ~/.zshrc;

git pull origin main

rm data/ec/prod2/*.html
rm data/ec/prod2/*.pdf
rm data/ec/prod2/*.xml

python workflows/parse_ec.py
git add *
git commit -m "parse_ec ($(date))"
git push origin main


# cp data/ec/test1/* /Volumes/2024-KING64/