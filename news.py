import requests
from bs4 import BeautifulSoup

def scraper(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    data = []
    articles = soup.find_all('c-wiz', {'jsrenderer': 'ARwRbe'})

    # Limit the loop to iterate only 5 times
    for idx, article in enumerate(articles):
        if idx >= 5:
            break
        
        try:
            image = article.find("figure").find("img").get("src")
        except:
            image = ""
        try:
            source_link_div = article.find('div', class_='XlKvRb')
            source_link = "https://news.google.com" + source_link_div.find('a')['href']
        except:
            source_link = ""

        try:
            title = article.find('h4').text
        except:
            title = ""

        external_links_element = article.find_all("a")
        external_headings_element = article.find_all("h4")
        external_headings_element.pop(0)
        external_links = {}
        for i, el in enumerate(external_links_element):
            try:
                external_links[external_headings_element[i].text] = "https://news.google.com" + el['href']
            except:
                external_links["Full Coverage"] = "https://news.google.com" + el['href']
        data.append({
            "image": image,
            "source link": source_link,
            "title": title,
            "external links": external_links
        })
    return data

url_list=["CAAqIggKIhxDQkFTRHdvSkwyMHZNRGxqTjNjd0VnSmxiaWdBUAE",
"CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB",
"CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB",
"CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB",
"CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB",
"CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB",
"CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB",
"CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ"]

value=input()
for url in url_list:
    urls = scraper("https://news.google.com/topics/"+url+"?hl=en-"+value+"&gl="+value+"&ceid="+value+"%3Aen")
    print(urls)