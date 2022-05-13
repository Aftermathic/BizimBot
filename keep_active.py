from flask import Flask
import os
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    while True:
        errors = open("error.txt", "r")
        if os.stat("error.txt").st_size == 0:
            return f"<h1>Bizim Bot Status: </h1>Errors: None"
        else:
            return f"<h1>Bizim Bot Status: </h1>Errors: {errors.read()}"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()