from scraper import ChosunScraper
import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect("news_data.db", isolation_level=None)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE  IF NOT EXISTS article (id text PRIMARY KEY, text text, image)"
    )
    scraper = ChosunScraper([])
    scraper._get_page_html(
        page_url="https://stackoverflow.com/questions/55953514/python-beautifulsoup-program-initialization"
    )
