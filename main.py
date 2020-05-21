from flask import Flask , render_template, jsonify, request, redirect, url_for
from json2html import *
import pandas as pd
from scrape import scrape_maps

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/', methods=['POST'])
def submit():
	if request.method == 'POST':
		file = request.form['filename']
		df = pd.read_csv(file)
		data = df[["Places"]].values

	scraped_data = scrape_maps(data)

	return jsonify(scraped_data)



if __name__== "__main__":
    app.run(debug=True)