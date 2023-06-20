import pandas as pd
import requests
import json
from dotenv import load_dotenv
import pyrebase
import yaml
import os
import random
import time

load_dotenv()
api_key = os.environ["FIREBASE_API_KEY"]
auth_domain = os.environ["FIREBASE_AUTH_DOMAIN"]
database_url = os.environ["FIREBASE_DATABASE_URL"]
storage_bucket = os.environ["FIREBASE_STORAGE_BUCKET"]

firebase_config = {
  "apiKey": api_key,
  "authDomain": auth_domain,
  "databaseURL": database_url,
  "storageBucket": storage_bucket
}
firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()

answer = storage.child("/fake_stocks/stock_dir.txt").download(path='gs://stock-storage-54197.appspot.com/', filename=f"stock_dir.txt")
stock_dir = open("stock_dir.txt", "r").read().strip()
all_stocks = stock_dir.split("\n")

def increment_price(cur_price):
  return cur_price + (((random.random() - 0.5) * 3) / 100) * cur_price

for stock in all_stocks:
  storage.child(f"/fake_stocks/{stock}.txt").download(path='gs://stock-storage-54197.appspot.com/', filename=f"{stock}.txt")
  if not os.path.isfile(f"{stock}.txt"):
    stock_file = open(f"{stock}.txt", "w") 
    prices = []
    current_price = random.randint(1, 50)
    prices.append(str(current_price) + ".00") 
    for i in range(99):
      new_price = increment_price(float(prices[0]))
      prices.insert(0, str(new_price))
    price_string = f"{stock}" + ": " + " ".join(prices)
    stock_file.write(price_string) 
    stock_file.close()
    storage.child(f"/fake_stocks/{stock}.txt").put(f"{stock}.txt") 

while True:
  for stock in all_stocks:
      storage.child(f"/fake_stocks/{stock}.txt").download(path='gs://stock-storage-54197.appspot.com/', filename=f"{stock}.txt")
      stock_file = open(f"{stock}.txt", "r")
      cur_price = float(stock_file.read().split(" ")[-1])
      stock_file.close()
      stock_file = open(f"{stock}.txt", "a")
      stock_file.write(" " + str(increment_price(cur_price)))
      stock_file.close()
      storage.child(f"/fake_stocks/{stock}.txt").put(f"{stock}.txt")
  time.sleep(3)