from flask import Flask , render_template, jsonify, request, redirect, url_for
from json2html import *
import pandas as pd
from scrape import scrape_maps
import csv

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/', methods=['POST'])
def submit():
	if request.method == 'POST':
		file = request.form['filename']

	df = pd.read_csv(file)

	if "Places" in df.columns:
		data = df[["Places"]].values
	else:
		return("ERROR!!! CSV File doesn't have a 'Places' Column. Input Locations in Places Column")

	scraped_data, place_id_data = scrape_maps(data)

	reviews_data = []
	location_data = []

	for key in scraped_data.keys():
		for x in scraped_data[key]["Reviews"]:
			reviews_data.append([key, x["name"], x["review"], x["date"], x["rating"]])

		location_data.append([key, scraped_data[key]["contact"], scraped_data[key]["location"], scraped_data[key]["rating"], scraped_data[key]["reviews_count"], str(scraped_data[key]["Time"])])


	reviews_data_fields = ['Location', 'Name', 'Review', 'Time', 'Rating']
	location_data_fields = ['Name', 'Contact', 'Address', 'Rating', 'Total Count', 'Timings']
	place_id_fields = ['Location Name', 'Place ID']

	filename = "static/data/Reviews_Data.csv"
	new_filename = "static/data/Location_Data.csv"
	place_id_file = "static/data/Place_ID_Data.csv"

	with open(filename, 'w', newline='', encoding='utf-8') as csvfile:   

		csvwriter = csv.writer(csvfile)   
		csvwriter.writerow(reviews_data_fields)   
		csvwriter.writerows(reviews_data)

	with open(new_filename, 'w', newline='', encoding='utf-8') as newcsvfile:   

		csvwriter = csv.writer(newcsvfile)   
		csvwriter.writerow(location_data_fields)   
		csvwriter.writerows(location_data)

	with open(place_id_file, 'w', newline='', encoding='utf-8') as placeidfile:   

		csvwriter = csv.writer(placeidfile)   
		csvwriter.writerow(place_id_fields)   
		csvwriter.writerows(place_id_data)

	
	return render_template("index.html", lol="visible")


if __name__== "__main__":
    app.run(debug=True)