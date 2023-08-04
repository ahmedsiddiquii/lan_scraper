from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys # Import the Keys class
import undetected_chromedriver as uc
import time

def scrape_google_maps(content_type, number_of_results):
    # Latitude and Longitude for Vancouver
    latitude = "49.2827"
    longitude = "-123.1207"

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

    print(len(cards))
    for c in cards[:number_of_results]:
        # Process the cards as needed
        print(c.get_attribute("href"))
        driver.get(c)
        name=driver.find_element(by="xpath",value='//h1[@class="DUwDvf lfPIob"]').text
        desc=driver.find_element(by="xpath",value='//div[@class="PYvSYb "]').text
        location=driver.find_element(by="xpath",value='//div[@class="Io6YTe fontBodyMedium kR99db "]').text
        contact=driver.find_elements(by="xpath",value='//div[@class="Io6YTe fontBodyMedium kR99db "]')
        for i in contact:
            phone=(i[5]).text
        web=driver.find_elements(by="xpath",value='//div[@class="Io6YTe fontBodyMedium kR99db "]')
        for i in web:
            website=(i[4]).text
        reviews=driver.find_elements(by="xpath",value='//div[@class="fontDisplayLarge"]').text
        print(name)
        print(desc)
        print(location)
        print(contact)
        print(phone)
        print(website)
        print(reviews)

    # Don't forget to close the driver when you're done
    driver.quit()

# Example usage
content_type = "restaurants" # Type of content to search for
number_of_results = 10 # Number of results to return

scrape_google_maps(content_type, number_of_results)
