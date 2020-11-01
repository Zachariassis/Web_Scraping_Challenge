from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import mission_to_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    news = mongo.db.news.find_one()
    return render_template("index.html", news=news)


@app.route("/scrape")
def scraper():
    news = mongo.db.news
    news_data = mission_to_mars.mars_news()
    news.update({}, news_data, upsert=True)

    return redirect("/", code=302)


if __name__=="__main__":
    app.run(debug=True)