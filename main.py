from flask import Flask , render_template, jsonify, request, redirect, url_for
from json2html import *
import pandas as pd
from test import WebDriver
import csv

app = Flask(__name__)

def structure_data(scraped_data):
	reviews_data = []
	location_data = []
	for key in scraped_data.keys():
		for x in scraped_data[key]["Reviews"]:
			reviews_data.append([key, x["name"], x["review"], x["date"], x["rating"]])

		location_data.append([key, scraped_data[key]["contact"], scraped_data[key]["location"], scraped_data[key]["rating"], scraped_data[key]["reviews_count"], str(scraped_data[key]["Time"]), scraped_data[key]["Popular Times"]["Sunday"], scraped_data[key]["Popular Times"]["Monday"], scraped_data[key]["Popular Times"]["Tuesday"], scraped_data[key]["Popular Times"]["Wednesday"], scraped_data[key]["Popular Times"]["Thursday"], scraped_data[key]["Popular Times"]["Friday"], scraped_data[key]["Popular Times"]["Saturday"]])

	return(reviews_data, location_data)



def create_files(reviews_data, location_data, place_id_data, reviews_data_fields, location_data_fields, place_id_fields):

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


@app.route("/")
def index():
	return render_template("index.html")

@app.route('/', methods=['POST'])
def submit():
	if request.method == 'POST':
		file = request.files['filename']

	df = pd.read_csv(file)

	if "Places" in df.columns:
		data = df[["Places"]].values
	else:
		return("ERROR!!! CSV File doesn't have a 'Places' Column. Input Locations in Places Column")

	obj = WebDriver()
	scraped_data, place_id_data = obj.scrape(data)

	reviews_data, location_data = structure_data(scraped_data)

	reviews_data_fields = ['Place ID', 'Name', 'Review', 'Time', 'Rating']
	location_data_fields = ['Place ID', 'Contact', 'Address', 'Rating', 'Total Count', 'Timings', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	place_id_fields = ['Location Name', 'Place ID']

	create_files(reviews_data, location_data, place_id_data, reviews_data_fields, location_data_fields, place_id_fields)

	
	return render_template("index.html", lol="visible")


if __name__== "__main__":
    app.run(debug=True)