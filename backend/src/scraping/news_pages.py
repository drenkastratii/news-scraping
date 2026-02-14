Sites = [
    {
        "portal": "BBC",
        "news_url": "https://www.bbc.com",
        "stop_phrases": ["Copyright","The BBC is not responsible","Read about our approach"],
        "news_headline":"h2[data-testid='card-headline']",
        "news_text": "main p"
    },
    {
        "portal": "CNN",
        "news_url": "https://edition.cnn.com",
        "stop_phrases": [],
        "news_headline": "span.container__headline-text",
        "news_text": "p.paragraph, p.paragraph--lite, p.paragraph-elevate"
    },
    {
        "portal": "NBC",
        "news_url": "https://www.nbcnews.com/latest-stories/",
        "stop_phrases": [],
        "news_headline": "h2[data-testid='wide-tease-headline']",
        "news_text": "p.body-graf"
    }
]