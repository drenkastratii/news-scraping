import requests
from bs4 import BeautifulSoup as bs
import csv
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from news_pages import Sites

PATH = r"C:\Users\Dren\Desktop\rit-final\backend\db "
CSV_FILE = "news.csv"

RESTART_TIME_MIN = 5

MAX_PORTALS_AT_ONCE = 5

news = []
seen_urls = set()
article_id = 1 
id_lock = Lock()
news_lock = Lock()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    )
}

def clean_text(text, stop_phrases):
    for phrase in stop_phrases:
        if phrase in text:
            text = text.split(phrase)[0]
    return text.strip()


def human_sleep():
    delay = random.uniform(2, 4)
    print(f"Human delay {delay:.1f}s ...")
    time.sleep(delay)


def get_next_id():
    global article_id
    with id_lock:
        val = article_id
        article_id += 1
    return val


def load_existing_news():
    global news, seen_urls, article_id
    csv_path = "{PATH}\\{CSV_FILE}"
    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get("news_url"):
                    continue
                news.append({
                    "id": int(row["id"]),
                    "portal": row["portal"],
                    "news_title": row["news_title"],
                    "news_url": row["news_url"],
                    "news_text": row["news_text"],
                })
                seen_urls.add(row["news_url"])
        if news:
            article_id = max(item["id"] for item in news) + 1
        print(f"Loaded {len(news)} existing articles from CSV. Next id = {article_id}")
    except Exception as e:
        print(f"[Could not load existing CSV] : {e}")


def scrape_portal(news_site):
    session = requests.Session()
    session.headers.update(HEADERS)

    local_results = []

    NEWS_URL = news_site["news_url"]
    headline_selector = news_site["news_headline"]
    portal = news_site["portal"]
    news_text_selector = news_site["news_text"]
    stop_phrases = news_site["stop_phrases"]

    print(f"[Starting portal: {portal}]")

    try:
        homepage = session.get(NEWS_URL, timeout=10).text
    except Exception as e:
        print(f"Error [{portal} homepage failed:", e, "]")
        return

    soup = bs(homepage, "lxml")
    headlines = soup.select(headline_selector)

    print(f"{portal}: {len(headlines)} headlines")

    for i, h in enumerate(headlines):
        title = h.get_text(strip=True)
        parent = h.find_parent("a")

        if not parent or not parent.get("href"):
            continue

        url = parent["href"]
        if url.startswith("/"):
            url = NEWS_URL.rstrip("/") + url

        if i > 0:
            human_sleep()

        print(f"[{portal}] {url}")

        try:
            r = session.get(url, timeout=10)
            html = r.text
        except Exception as e:
            print(f"Error [{portal} Article failed:", e, "]")
            continue

        if not html or len(html) < 500:
            continue

        article_soup = bs(html, "lxml")
        paragraphs = article_soup.select(news_text_selector)
        article_text = " ".join(p.get_text(strip=True) for p in paragraphs)

        if len(article_text) < 200:
            continue

        local_results.append({
            "portal": portal,
            "news_title": title,
            "news_url": url,
            "news_text": clean_text(article_text, stop_phrases)
        })

    with news_lock:
        for item in local_results:
            if item["news_url"] in seen_urls:
                continue
            seen_urls.add(item["news_url"])
            item["id"] = get_next_id()
            news.append(item)

    print(f"Finished portal: {portal}")

load_existing_news()

while True:
    with ThreadPoolExecutor(max_workers=MAX_PORTALS_AT_ONCE) as executor:
        futures = [executor.submit(scrape_portal, site) for site in Sites]
        for _ in as_completed(futures):
            pass

    with open(f"{PATH}\\{CSV_FILE}", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "portal", "news_title", "news_url", "news_text"]
        )
        writer.writeheader()
        writer.writerows(news)

    print("TOTAL ARTICLES:", len(news))
    time.sleep(RESTART_TIME_MIN * 60)