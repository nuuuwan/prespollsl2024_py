#!/bin/zsh
source ~/.zshrc;

git pull origin main
python workflows/parse_ec.py
git add *
git commit -m "parse_ec ($(date))"
git push origin main


cp data/ec/test1/* /Volumes/2024-KING64/