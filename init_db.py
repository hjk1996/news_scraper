import sqlite3
import pandas as pd
from glob import glob
import os
from model import ArticleInfo

excel_files: list[str] = glob("./raw_data/*.xlsx")
columns = {
    "id": "TEXT",
    "date": "TEXT",
    "press": "TEXT",
    "reporter": "TEXT",
    "title": "TEXT",
    "category1": "TEXT",
    "category2": "TEXT",
    "category3": "TEXT",
    "event_type_1": "TEXT",
    "event_type_2": "TEXT",
    "event_type_3": "TEXT",
    "related_people": "TEXT",
    "related_location": "TEXT",
    "related_institutions": "TEXT",
    "keywords": "TEXT",
    "features": "TEXT",
    "content_preview": "TEXT",
    "article_url": "TEXT",
    "excluded": "BLOB",
    "content": "TEXT",
    # "search_keyword": "TEXT",
    "image_dirs": "TEXT",
    # "hash_id": "TEXT",
}


if __name__ == "__main__":

    con = sqlite3.connect("./news.db")
    for file in excel_files:
        search_keyword = os.path.basename(file).split(".")[0]
        news_data = pd.read_excel(file)
        news_data["content"] = None
        # news_data["search_keyword"] = search_keyword
        news_data["image_dirs"] = None
        # news_data["hash_id"] = None
        news_data.columns = list(columns.keys())
        # news_data["hash_id"] = news_data.apply(
        #     lambda x: str(hash((x["press"], x["title"]))), axis=1
        # )
        news_data.columns = list(columns.keys())
        news_data.dropna(axis=0, inplace=True, subset=["article_url"])
        news_data.to_sql("news", con, if_exists="append", index=False, dtype=columns)
