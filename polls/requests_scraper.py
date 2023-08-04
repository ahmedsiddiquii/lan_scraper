from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import time

def scrape_google_maps(content_type, number_of_results):
    # Latitude and Longitude for Vancouver
    latitude = "49.2827"
    longitude = "-123.1207"

    # Construct the URL for Google Maps search
    url = f"https://www.google.com/maps/search/{content_type}/@{latitude},{longitude},13z/data=!3m1!4b1?entry=ttu"

    # Chrome options
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless") # Run in headless mode
    chrome_options.add_argument("user-agent=Your-Custom-User-Agent") # Set custom user agent

    # Start a Selenium web driver
    driver = uc.Chrome(options=chrome_options)

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
        time.sleep(0.5) # Reduced sleep time
        cards = driver.find_elements(By.XPATH, "//a[@class='hfpxzc']")

    print(len(cards))
    links=[]
    for link in cards[:number_of_results]:
        links.append(link.get_attribute("href"))
    for link in links:

        driver.get(link)
        time.sleep(2) # Reduced sleep time
        name = driver.find_element(by="xpath", value='//h1[@class="DUwDvf lfPIob"]').text
        print(name)
        try:
            desc = driver.find_element(by="xpath", value='//div[@class="PYvSYb "]').text
            print(desc)
        except:
            pass
        location = driver.find_element(by="xpath", value='//div[@class="Io6YTe fontBodyMedium kR99db "]').text
        contacts = driver.find_elements(by="xpath", value='//div[@class="Io6YTe fontBodyMedium kR99db "]')
        phone_numbers = [contact.text for contact in contacts]
        reviews = driver.find_element(by="xpath", value='//div[@class="fontDisplayLarge"]').text
        print(location)
        print(phone_numbers[5])
        print(phone_numbers[4])
        print(reviews)

    # Don't forget to close the driver when you're done
    driver.quit()

# Example usage
content_type = "restaurants" # Type of content to search for
number_of_results = 10 # Number of results to return

scrape_google_maps(content_type, number_of_results)
