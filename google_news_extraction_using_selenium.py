from selenium import webdriver
from selenium.webdriver.common.by import By
import time



def google_news_scraper(website):


    driver = webdriver.Chrome()
    driver.get(website)

    data = []

    image_elements = driver.find_elements(By.XPATH, '//figure[@class="K0q4G P22Vib"]//img')
    latest_news_elements = driver.find_elements(By.XPATH, '//h4[@class="gPFEn"]')
    hyperlink_elements = driver.find_elements(By.XPATH, '//a')

    for count, (image_element, news_element, hyperlink_element) in enumerate(zip(image_elements, latest_news_elements, hyperlink_elements)):
        news_text = news_element.text
        img_src = image_element.get_attribute('srcset').split()[0]
        href = hyperlink_element.get_attribute('href')
        
        article_data = {
            "img": img_src,
            "description": news_text,
            "hyperlink": href
        }
        
        data.append(article_data)

        print("Image:", img_src)
        print("Description:", news_text)
        print("Hyperlink:", href)
        print("=" * 40)



    # Convert data list to a JSON string
    import json
    json_data = json.dumps(data, indent=2)

    # Print JSON data
    print(json_data)

    # Save JSON data to a file
    with open('news_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


    time.sleep(5)

    driver.quit()

website = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=en-PK&gl=PK&ceid=PK%3Aen'
print("Printing the result: ", google_news_scraper(website))