git pull origin main

rm C:\Users\ASUS\AppData\Local\Temp\election-2024-09-21\images\*
rm  C:\Users\ASUS\AppData\Local\Temp\election-2024-09-21\hidden_data\*

python .\workflows\media\build_tweet.py 

firefox_quit