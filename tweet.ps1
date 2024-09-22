
git pull origin main

git add * 
git commit -m "Update tweet"

git push origin main

python .\workflows\media\build_tweet.py --TWTR_BEARER_TOKEN="$env:TWTR_BEARER_TOKEN" --TWTR_API_KEY="$env:TWTR_API_KEY" --TWTR_API_KEY_SECRET="$env:TWTR_API_KEY_SECRET" --TWTR_ACCESS_TOKEN="$env:TWTR_ACCESS_TOKEN" --TWTR_ACCESS_TOKEN_SECRET="$env:TWTR_ACCESS_TOKEN_SECRET"

git pull origin main