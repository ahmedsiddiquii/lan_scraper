from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run the browser in headless mode (no UI)

def scrpe(data):
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.google.com/')
    driver.maximize_window()
    
    search_box = driver.find_element(by='xpath', value='//textarea[@class="gLFyf"]')
    search_box.send_keys(data)
    search_box.send_keys(Keys.ENTER)
    time.sleep(7)
    
    scroll_height = 1000
    num_scrolls = 2 

    for _ in range(num_scrolls):
        driver.execute_script(f'window.scrollBy(0, {scroll_height});')

    desc_elements = driver.find_elements(by='xpath', value='//div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"]//span')
    descriptions = [des_element.text for des_element in desc_elements]

    time.sleep(5)

    link_elements = driver.find_elements(by='xpath', value='//div[@class="Z26q7c UK95Uc jGGQ5e"]//a')
    links = [link_element.get_attribute('href') for link_element in link_elements]

    data_list = []

    for des, link in zip(descriptions, links):
        data_dict = {
            'description': des,
            'link': link
        }
        data_list.append(data_dict)

    driver.quit()
    return data_list
