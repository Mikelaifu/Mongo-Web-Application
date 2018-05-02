from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)


@app.route("/")
def index():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.delete_many({})
    mars.insert_one(mars_data)
    return redirect("http://127.0.0.1:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
