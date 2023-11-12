from flask import Flask
import toolkit as ftk

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Financial Toolkit</p>"

@app.route('/ticker/<ticker>')
def get_price(ticker):
    return ftk.get_yahoo(ticker).to_json()