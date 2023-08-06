from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys # Import the Keys class
import undetected_chromedriver as uc
import time
import re
from .models import *


def get_direction_url(url: str) -> str:
    try:
        # Extract latitude and longitude from URL
        lat, lon = re.findall(r'!8m2!3d([\d.-]+)!4d([\d.-]+)', url)[0]

        # Extract location name from URL (if required for other purposes)
        location_name_match = re.search(r'maps/place/([^/]+)', url)
        location_name = location_name_match.group(1).replace('+', ' ') if location_name_match else ""

        # Create direction URL from current location to the specified location
        direction_url = f"https://www.google.com/maps/dir/Current+Location/{lat},{lon}/"

        return direction_url
    except:
        return "Invalid URL or no coordinates found in URL."


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


    print(len(cards))
    data=[]
    direction_link=driver.find_elements("xpath","//a[@class='hfpxzc']")
    names= driver.find_elements("xpath","//div[@class='qBF1Pd fontHeadlineSmall ']")
    ratings=driver.find_elements("xpath","//span[@class='MW4etd']")
    categories = driver.find_elements("xpath","//div[@class='UaQhfb fontBodyMedium']//div[@class='W4Efsd'][2]//div[@class='W4Efsd'][1]/span[1]")
    locations= driver.find_elements("xpath","//div[@class='UaQhfb fontBodyMedium']//div[@class='W4Efsd'][2]//div[@class='W4Efsd'][1]/span[2]/span[2]")
    descriptions= driver.find_elements("xpath","//div[@class='UaQhfb fontBodyMedium']//div[@class='W4Efsd'][2]//div[@class='W4Efsd'][2]/span/span")
    statuses= driver.find_elements("xpath","//div[@class='UaQhfb fontBodyMedium']//div[@class='W4Efsd'][2]//div[@class='W4Efsd'][3]/span/span/span[1]")
    # timings = driver.find_elements("xpath","//div[@class='UaQhfb fontBodyMedium']//div[@class='W4Efsd'][2]//div[@class='W4Efsd'][3]/span/span/span[2]")

    for i in range(len(direction_link[:number_of_results])):
        print(i)
        dir_url=get_direction_url(direction_link[i].get_attribute("href"))
        name=names[i].text
        rating=ratings[i].text
        category=categories[i].text
        location=locations[i].text
        description=descriptions[i].text
        try:
            status=driver.find_element("xpath",
                                       f"(//a[@class='hfpxzc'])[{i+1}]/following-sibling::div[2]//div[@class='UaQhfb fontBodyMedium']//div[@class='W4Efsd'][2]//div[@class='W4Efsd'][3]/span/span/span[1]").text
        except:
            status=""
        try:
            timing=driver.find_element("xpath",f"(//a[@class='hfpxzc'])[{i+1}]/following-sibling::div[2]//div[@class='UaQhfb fontBodyMedium']//div[@class='W4Efsd'][2]//div[@class='W4Efsd'][3]/span/span/span[2]").text
        except:
            timing=""
        temp={"direction":dir_url,"name":name,"rating":rating,"category":category,"location":location,
              "description":description,"status":status,"timing":timing,"query":query}
        obj=Google_data(**temp)
        obj.save()

    # Don't forget to close the driver when you're done
    driver.quit()
