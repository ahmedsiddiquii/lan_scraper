from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys # Import the Keys class
import undetected_chromedriver as uc
import time
from .models import *




def scrape_google_maps(content_type, number_of_results, latitude, longitude,query):
    # Latitude and Longitude for Vancouver
    #latitude = "49.2827"
    #longitude = "-123.1207"
    # Construct the URL for Google Maps search
    url = f"https://www.google.com/maps/search/{content_type}/@{latitude},{longitude},13z/data=!3m1!4b1?entry=ttu"
    # Start a Selenium web driver
    driver = uc.Chrome()
    # Navigate to the URL
    driver.get(url)
    time.sleep(2) # Allow some time for the page to load
    # Find the scrollable element (the whole body in this case)
    scrollable_element = driver.find_element(By.XPATH, "//div[@role='feed']")
    # Create an ActionChains object
    actions = ActionChains(driver)
    # Find the cards
    cards = driver.find_elements(By.XPATH, "//a[@class='hfpxzc']")
    cards[0].click()
    while len(cards) < number_of_results:
        # Perform a scroll down action
        actions.move_to_element(scrollable_element).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1) # Allow some time for new cards to load
        cards = driver.find_elements(By.XPATH, "//a[@class='hfpxzc']")

        print(cards)
    print(len(cards))
    names=driver.find_elements("xpath","//div[@class='qBF1Pd fontHeadlineSmall ']")
    links=[]
    for l in cards:
        links.append(l.get_attribute('href'))
    for c in links[:number_of_results]:
        # Process the cards as needed

        driver.get(c)

        time.sleep(5)
        name=driver.find_element(by="xpath",value='//h1[@class="DUwDvf lfPIob"]').text
        print(name)
        try:
            desc=driver.find_element(by="xpath",value='//div[@class="PYvSYb "]').text
            print(desc)
        except:
            desc=""
            pass
        location=driver.find_element(by="xpath",value='//div[@class="Io6YTe fontBodyMedium kR99db "]').text
        contacts = driver.find_elements(by="xpath", value='//div[@class="Io6YTe fontBodyMedium kR99db "]')
        phone_numbers = []
        for contact in contacts:
            phone_numbers.append(contact.text)
        reviews=driver.find_element(by="xpath",value='//div[@class="fontDisplayLarge"]').text
        print(location)
        print(phone_numbers[5])
        print(phone_numbers[4])
        print(reviews)
        obj=Google_data()
        obj.name=name
        obj.description=desc
        obj.location=location
        obj.phone=contact.text
        obj.website=""
        obj.reviews=reviews
        obj.query_id=query

    # Don't forget to close the driver when you're done
    driver.quit()
# Example usage
content_type = "restaurants" # Type of content to search for
number_of_results = 10 # Number of results to return


# def get_pending_queries():
#     # Query your database to get pending queries
#     pending_queries = Queries.get_pending_queries()
#     return pending_queries
#
# def process_pending_queries():
#     pending_queries = get_pending_queries()
#     for query in pending_queries:
#         longitude = query['longitude']
#         latitude = query['latitude']
#         content_type = query['type']
#         number_of_results = 10  # You can set the desired number of results here
#
#         # Call the scraper function with the extracted data
#         scrape_google_maps(content_type, number_of_results, latitude, longitude)
#
# # Run the process
# process_pending_queries()

