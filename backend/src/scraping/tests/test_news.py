import requests
from bs4 import BeautifulSoup as bs
import csv
from urllib.parse import urljoin


path = r"C:\Users\Dren\Desktop\rit-final\backend\db"
cnn_file_csv = "test-news.csv"

news = []
article_id = 1

Sites = [
    {
        "portal": "BBC",
        "news_url": "https://www.bbc.com",
        "stop_phrases": ["Copyright","The BBC is not responsible","Read about our approach"],
        "news_headline":"h2[data-testid='card-headline']",
        "news_text": "main p"
    }
]

for news_site in Sites:
    portal = news_site["portal"]
    news_url = news_site["news_url"]
    news_headline = news_site["news_headline"]
    news_text = news_site["news_text"]
    stop_phrases = news_site["stop_phrases"]

    def clean_text(text):
        for phrase in stop_phrases:
            if phrase in text:
                text = text.split(phrase)[0]
        return text.strip()

    src = requests.get(news_url).text
    soup = bs(src, "lxml")

    headlines = soup.select(news_headline)

    for headline in headlines:
        parent = headline.find_parent("a")
        if not parent or not parent.get("href"):
            continue
        title = headline.get_text(strip=True)
        url = urljoin(news_url + "/", parent["href"])

        article_src = requests.get(url).text
        article_soup = bs(article_src, "lxml")

        paragraphs = article_soup.select(news_text)
        article_text = " ".join(p.text.strip() for p in paragraphs)
        article_text = clean_text(article_text)

        news.append({
            "id" : article_id,
            "portal":portal,
            "news_title": title,
            "news_url": url,
            "news_paragraphs": article_text
        })

        article_id += 1


with open(f"{path}\\{cnn_file_csv}", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["id","portal","news_title","news_url","news_paragraphs"]
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    csv_writer.writeheader()
    csv_writer.writerows(news)


print("\nTOTAL ARTICLES:", len(news))
