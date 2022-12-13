from bs4 import BeautifulSoup as BS
from requests_html import HTMLSession
import csv

domain = "url" # website url
request = "get" # website page get parameter
pages = 2 #  number of website pages
headerFields = ["Title", "Image", "Images", "Description", "New price", "Old price"]
try:
    print("Collecting data...")
    file = open("Catalog.csv", "w")
    csvwriter = csv.writer(file)
    csvwriter.writerow(headerFields)
    for i in range(pages):
        items = 0
        page = i + 1
        url_1 = domain + request + str(page)
        session_1 = HTMLSession()
        page_1 = session_1.get(url_1)
        page_1.html.render()
        html_1 = BS(page_1.html.html, 'html.parser')
        # custom for each
        for el in html_1.select(".products-list"):
            for link in el.select(".product-card-image > a"):
                url_2 = domain + link.get("href")
                session_2 = HTMLSession()
                page_2 = session_2.get(url_2)
                page_2.html.render()
                html_2 = BS(page_2.html.html, 'html.parser')
                title = html_2.select(".info-block > .title")[0].text.strip() 
                img_link = html_2.select(".slide-wrapper > .slide-item > img")[0].get("src")
                img_links = ""
                for img in html_2.select(".photo-navigation > .photo-nav-item > img"):
                    img_links = img_links + img.get("src") + "\n"
                description = html_2.select(".user-description")[0].text.strip()
                new_price = html_2.select(".total-price > span")[0].text.strip()
                old_price = html_2.select(".old-price")[0].text.strip()
                csvwriter.writerow([title, img_link, img_links, description, new_price, old_price])
                items += 1
                print("page: " + str(page) + "/" + str(pages) + " items: " + str(items) + "/" + str(len(el)))
finally:
    file.close()
    print("Complete!")
