import requests
from bs4 import BeautifulSoup

url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=en-PK&gl=PK&ceid=PK%3Aen"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")



data = []
articles=  soup.find_all('c-wiz', {'jsrenderer': 'ARwRbe'})

for article in articles:
    try:
        image= article.find("figure").find("img").get("src")
    except:
        image = ""
    try:
        # Here's the translation of your XPath to BeautifulSoup
        source_link_div = article.find('div', class_='XlKvRb')
        source_link = "https://news.google.com"+source_link_div.find('a')['href']
    except:
        source_link = ""

    try:

        title = article.find('h4').text
    except:
        title = ""

    external_links_element=article.find_all("a")
    external_headings_element = article.find_all("h4")
    external_headings_element.pop(0)
    external_links = {}
    for i,el in enumerate(external_links_element):
        try:
            external_links[external_headings_element[i].text]="https://news.google.com"+el['href']
        except:
            external_links["Full Coverage"] = "https://news.google.com"+el['href']
    data.append({"image":image,
                 "source link":source_link,
                 "title":title,
                 "external links":external_links})
