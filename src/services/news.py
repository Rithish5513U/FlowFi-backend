from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()
key = os.getenv("NEWS_API")

class News:
    def __init__(self):
        self.key = key
        self.newsapi = NewsApiClient(api_key=key)

    # for getting the top headlines based on user preferences
    def get_top_headlines(self, preferences: List[str]) -> List[dict]:
        """
        Inputs:
            List of preferences -> str
        Outputs:
            List of dictionaries containing the news data
        """
        threshold = 2
        if len(preferences) <= 2:
            threshold = 5
        
        required_data = []
        for preference in preferences:
            top_headlines = self.newsapi.get_top_headlines(
                q=preference, language="en"
            )
            result = top_headlines["articles"]
            cnt = 0
            for each in result:
                if cnt == threshold:
                    break
                cnt += 1
                required_data.append(
                    {
                        "author": each["author"],
                        "title": each["title"],
                        "description": each["description"],
                        "url": each["url"],
                        "urlToImage": each["urlToImage"],
                    }
                )
        return required_data

    # for getting all the news based on user preferences
    def get_everything(self, preferences: List[str]) -> List[dict]:
        """
        Inputs:
            List of preferences -> str
        Outputs:
            List of dictionaries containing the news data
        """
        result = []
        threshold = 5
        for preference in preferences:
            everything = self.newsapi.get_everything(language="en", q=preference)
            required = everything["articles"]
            cnt = 0
            
            for each in required:
                if cnt == threshold:
                    break
                cnt += 1
                result.append(
                    {
                        "author": each["author"],
                        "publishedAt": each["publishedAt"],
                        "title": each["title"],
                        "description": each["description"],
                        "url": each["url"],
                        "urlToImage": each["urlToImage"],
                    }
                )
        return result