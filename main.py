from scraper import DongAScraper
import sqlite3
from glob import glob


if __name__ == "__main__":

    con = sqlite3.connect('./news.db')
    cursor = con.cursor()

    scraper = DongAScraper(cursor)
    scraper.scrape()
