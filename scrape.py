from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

data = ["ChIJZ-DLDJ9HrTsR681u8-Ui8v4", "ChIJtV8FufYdDTkRwKMeayYLwYE"]

PATH = "C:\Program Files (x86)\chromedriver.exe"

location_data = {}

for place_id in data:
	driver = webdriver.Chrome(PATH)
	url = "https://www.google.com/maps/search/?api=1&query=<address>&query_place_id={0}".format(place_id)

	location_data[place_id] = {}

	driver.get(url)

	time.sleep(10)

	if(len(list(driver.find_elements_by_class_name("cX2WmPgCkHi__section-info-hour-text")))!=0):
		element = driver.find_element_by_class_name("cX2WmPgCkHi__section-info-hour-text")
		driver.implicitly_wait(5)
		ActionChains(driver).move_to_element(element).click(element).perform()

	avg_rating = driver.find_element_by_class_name("section-star-display")
	total_reviews = driver.find_element_by_class_name("section-rating-term")
	address = driver.find_element_by_css_selector("[data-section-id='ad']")
	phone_number = driver.find_element_by_css_selector("[data-section-id='pn0']")
	days = driver.find_elements_by_css_selector("[class='lo7U087hsMA__row-header']")
	times = driver.find_elements_by_css_selector("[class='lo7U087hsMA__row-interval']")


	location_data[place_id]["rating"] = avg_rating.text
	location_data[place_id]["reviews_count"] = total_reviews.text[1:-1]
	location_data[place_id]["location"] = address.text
	location_data[place_id]["contact"] = phone_number.text

	location_data[place_id]["Time"] = {}

	day = [a.text for a in days]
	open_close_time = [a.text for a in times]

	for i, j in zip(day, open_close_time):
		location_data[place_id]["Time"][i] = j

	driver.quit()


print(location_data)