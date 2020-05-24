from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


def scrape_maps(data):

	PATH = "chromedriver.exe"

	options = Options()
	options.add_argument("--headless")

	location_data = {}
	place_id_data = []

	for id in data:

		search_field = id[0]

		google_driver = webdriver.Chrome(PATH, chrome_options=options)

		google_driver.get("https://www.google.com")

		time.sleep(2)

		search = google_driver.find_element_by_name("q")
		search.send_keys(search_field)

		time.sleep(5)

		try:
			text = google_driver.find_element_by_css_selector("[class='jKWzZXdEJWi__suggestions-inner-container']")
			text.click()
		except:
			search.send_keys(Keys.RETURN)


		time.sleep(5)

		try:
			place_id_loc = google_driver.find_element_by_css_selector("[id='wrkpb']")
			final_place_id = place_id_loc.get_attribute("data-pid")
			place_id = final_place_id

			place_id_data.append([search_field, place_id])

			google_driver.quit()

		except Exception as e :
			google_driver.quit()
			place_id_data.append([search_field, "NA"])
			continue


		url = "https://www.google.com/maps/search/?api=1&query=<address>&query_place_id={0}".format(place_id)

		driver = webdriver.Chrome(PATH, chrome_options=options)

		location_data[place_id] = {}
		location_data[place_id]["rating"] = "NA"
		location_data[place_id]["reviews_count"] = "NA"
		location_data[place_id]["location"] = "NA"
		location_data[place_id]["contact"] = "NA"
		location_data[place_id]["Time"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
		location_data[place_id]["Reviews"] = []


		try:
			driver.get(url)

		except Exception as e:
			driver.quit()
			continue

		time.sleep(10)

		if(len(list(driver.find_elements_by_class_name("cX2WmPgCkHi__section-info-hour-text")))!=0):
			element = driver.find_element_by_class_name("cX2WmPgCkHi__section-info-hour-text")
			driver.implicitly_wait(5)
			ActionChains(driver).move_to_element(element).click(element).perform()

		try:
			avg_rating = driver.find_element_by_class_name("section-star-display")
			total_reviews = driver.find_element_by_class_name("section-rating-term")
			address = driver.find_element_by_css_selector("[data-section-id='ad']")

			try:
				phone_number = driver.find_element_by_css_selector("[data-section-id='pn0']")
			except:
				pass

			days = driver.find_elements_by_class_name("lo7U087hsMA__row-header")
			times = driver.find_elements_by_class_name("lo7U087hsMA__row-interval")

		except Exception as e:
			pass

		try:
			location_data[place_id]["rating"] = avg_rating.text
			location_data[place_id]["reviews_count"] = total_reviews.text[1:-1]
			location_data[place_id]["location"] = address.text

			try:
				location_data[place_id]["contact"] = phone_number.text
			except:
				pass
				
			day = [a.text for a in days]
			open_close_time = [a.text for a in times]

		except Exception as e:
			pass


		try:
			for i, j in zip(day, open_close_time):
				location_data[place_id]["Time"][i] = j
		except Exception as e:
			pass


		try:
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "allxGeDnJMl__button")))

			element = driver.find_element_by_class_name("allxGeDnJMl__button")
			element.click()
		except:
			driver.quit()
			continue

		time.sleep(5)

		try:

			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))

			pause_time = 2
			max_count = 5
			x = 0

			while(x<max_count):

				scrollable_div = driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')

				driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)

				time.sleep(pause_time)

				x=x+1

		except:
			driver.quit()

		try:
			element = driver.find_elements_by_class_name("section-expand-review")
			for i in element:
				i.click()
		except Exception as e:
			pass


		try:
			review_names = driver.find_elements_by_class_name("section-review-title")
			review_text = driver.find_elements_by_class_name("section-review-review-content")
			review_dates = driver.find_elements_by_css_selector("[class='section-review-publish-date']")
			review_stars = driver.find_elements_by_css_selector("[class='section-review-stars']")

			review_stars_final = []

			for i in review_stars:
				review_stars_final.append(i.get_attribute("aria-label"))

			review_names_list = [a.text for a in review_names]
			review_text_list = [a.text for a in review_text]
			review_dates_list = [a.text for a in review_dates]
			review_stars_list = [a for a in review_stars_final]


			for (a,b,c,d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
				location_data[place_id]["Reviews"].append({"name":a, "review":b, "date":c, "rating":d})

		except Exception as e:
			pass


		driver.quit()

	return(location_data, place_id_data)
