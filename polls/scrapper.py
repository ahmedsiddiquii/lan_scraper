import time
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


 # Set up the Chrome webdriver


# Load the page
#search_name = 'lulu'
#latitude = '@41.5587382'
#longitude = '-133.3127447'


# scrapper.py


def scrape_data_from_google_maps(data):
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Run the browser in headless mode (no UI)
    driver = webdriver.Chrome(options=options)
    
    driver.get(data)
    driver.maximize_window()
    click_button = driver.find_elements(by='xpath', value='//div[@class="Nv2PK Q2HXcd THOPZb "]')
    scraped_data = []  # Initialize an empty list to store scraped data

    for i in click_button:
        i.click()
        time.sleep(15)
        name = driver.find_element(by='xpath', value='//h1[@class="DUwDvf lfPIob"]').text
        address = driver.find_element(by='xpath', value='//div[@class="Io6YTe fontBodyMedium kR99db "]').text
        time.sleep(5)
        reviews_list = []  # Initialize an empty list to store reviews

        try:
            reviews = driver.find_elements(by='xpath', value='//div[@class="MyEned"]')
            for review in reviews:
                review_text = review.text
                reviews_list.append(review_text)  # Append each review to the list
                print(review_text, "review")

        except:
            pass

        # Create a dictionary with the scraped data for each entry
        entry_data = {
            "name": name,
            "address": address,
            "reviews": reviews_list,
        }

        # Append the entry data to the list of scraped data
        scraped_data.append(entry_data)
    return scraped_data

      # Return the list of dictionaries containing scraped data
