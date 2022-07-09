import sqlite3
import pandas as pd
from glob import glob

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
        "image_urls": "BLOB",
    }

    con = sqlite3.connect("./news.db")
    for file in excel_files:
        news_data = pd.read_excel(file)
        news_data["content"] = None
        news_data["image_urls"] = None
        news_data.columns = list(columns.keys())

        news_data.to_sql(
            "meta_data", con, if_exists="append", index=False, dtype=columns
        )
