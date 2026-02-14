from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import news_router

version = "v1"

app = FastAPI(
    version=version,
    title="News Scraping"
)

app.include_router(news_router, prefix='/news')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)