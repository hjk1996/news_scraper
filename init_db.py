import sqlite3
import pandas as pd
from glob import glob
import os

# SCHEMA = 'CREATE TABLE "news_data" ("id" TEXT PRIMARY KEY, "date" TEXT NOT NULL, "press" TEXT NOT NULL,"reporter" TEXT,"title" TEXT NOT NULL,"category1" TEXT,"category2" TEXT,"category3" TEXT,"event_type_1" TEXT,"event_type_2" TEXT,"event_type_3" TEXT,"related_people" TEXT,"related_location" TEXT,"related_institutions" TEXT,"keywords" TEXT,"features" TEXT,"content_preview" TEXT,"article_url" TEXT NOT NULL, "excluded" BLOB,"content" TEXT,"image_urls" BLOB)'

if __name__ == "__main__":
    excel_files: list[str] = glob("./data/*.xlsx")
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
        "search_keyword": "TEXT",
        "image_dirs": "BLOB",
    }

    con = sqlite3.connect("./news.db")
    for file in excel_files:
        search_keyword = os.path.basename(file).split(".")[0]
        news_data = pd.read_excel(file)
        news_data["content"] = None
        news_data["search_keyword"] = search_keyword
        news_data["image_dirs"] = None
        news_data.columns = list(columns.keys())
        news_data.dropna(axis=0, inplace=True, subset=["article_url"])
        news_data.to_sql("news", con, if_exists="append", index=False, dtype=columns)
