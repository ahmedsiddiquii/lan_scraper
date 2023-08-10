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
links = soup.select_one("c-wiz[jsrenderer='ARwRbe']")
print(len(links))
for anchor in links:
    
    if anchor:
        link_length = len(anchor)
        print(f"Length of link: {link_length}")


# img = soup.find_all("img", class_="Quavad")

# for images in img:
#     image = images.get("src")



# title=soup.find_all("h4", class_="gPFEn")
# for titles in title:
#     tit=titles.text
    
#     data_article={
#         "title":tit,
#         "image": image,
#         "Links": link,
#     }
    
#     data.append(data_article)
    
#     import json
#     json_data = json.dumps(data, indent=2)

#     print(json_data)
    