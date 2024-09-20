git pull origin main
python workflows/parse_ec.py
git add *
git commit -m "parse_ec ($(date))"
git push origin main