from flask import Flask , render_template, jsonify, request, redirect, url_for
from json2html import *
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/', methods=['POST'])
def submit():
	if request.method == 'POST':
		file = request.form['filename']
		df = pd.read_csv(file)

	return df.Places[1]



if __name__== "__main__":
    app.run(debug=True)