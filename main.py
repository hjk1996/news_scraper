from scraper import ChosunScraper
import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect("news.db", isolation_level=None)
    cursor = conn.cursor()
    scraper = ChosunScraper(cursor)