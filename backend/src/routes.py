from fastapi import APIRouter, status
import csv

news_router = APIRouter()
NEWS_PATH = r"C:\Users\Dren\Desktop\rit-final\backend\db\news.csv"
AI_NEWS_PATH = r"C:\Users\Dren\Desktop\rit-final\backend\db\news_modified.csv"


@news_router.get("/", status_code=status.HTTP_200_OK)
def get_news():

    news_list = []

    with open(NEWS_PATH , mode='r', newline='', encoding='utf-8') as file:
        csvFile = csv.DictReader(file)
        
        for row in csvFile:
            news_item = {
                'news_portal' : row["portal"],
                'news_title' : row["news_title"],
                'news_text' : row["news_text"][:500]
            }
            
            news_list.append(news_item)

    return news_list 


@news_router.get("/ai-generated", status_code=status.HTTP_200_OK)
def get_ai_news():

    ai_news_list = []

    with open(AI_NEWS_PATH, mode='r', newline='', encoding='utf-8') as file:
        csvFile = csv.DictReader(file)
        
        for row in csvFile:
            news_item = {
                'news_portal' : row["portal"],
                'news_title' : row["news_title"],
                'news_text' : row["news_text"]
            }
            
            ai_news_list.append(news_item)

    return ai_news_list 