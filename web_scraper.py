import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

books_data = []

for page in range(1, 51):
    print(f"Scraping Page {page}...")

    url = BASE_URL.format(page)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to load Page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()
        rating = book.p["class"][1]

        books_data.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating
        })

    time.sleep(1)

df = pd.DataFrame(books_data)

df.to_csv("books_dataset.csv", index=False)

print("\nScraping Completed Successfully!")
print(f"Total Books Scraped: {len(df)}")
