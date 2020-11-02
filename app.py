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
    facts = mongo.db.facts.find_one()
    if facts is None:
        facts=facts
    else:
        facts=facts['Data']


    return render_template("index.html", news=news, facts=facts)


@app.route("/scrape")
def scraper():
    news = mongo.db.news
    facts = mongo.db.facts
    news_data = mission_to_mars.mars_news()

    featured_url = mission_to_mars.scrape_images()
    hemi= mission_to_mars.scrape_hemi()
    fact_data = {'Data': mission_to_mars.scrape_facts()}

    news_data={"Title": news_data.Title, "Body": news_data.Body, "Featured": featured_url,
               "HemiTitle": hemi['Title'].tolist() ,"HemiURL": hemi['Img_url'].tolist()}

    news.update({}, news_data, upsert=True)
    facts.update({}, fact_data, upsert=True)

    return redirect("/", code=302)


if __name__=="__main__":
    app.run(debug=True)