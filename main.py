from numpy import choose
from scraper import DongAScraper, ChoongAngScraper, KyunghyangScraper
import sqlite3
from glob import glob


if __name__ == "__main__":

    con = sqlite3.connect("./news.db")
    cursor = con.cursor()

    # scraper = DongAScraper(cursor)
    # scraper.scrape()

    # scraper = ChoongAngScraper(cursor)
    # scraper.scrape()

    scraper = KyunghyangScraper(cursor, need_driver=True)
    scraper.scrape()
    # html = scraper._get_page_html_from_driver(
    #     "https://www.khan.co.kr/national/court-law/article/202207101908001"
    # )
    # urls = scraper._get_article_image_urls(html)
    # text = scraper._get_article_text(html)
    # print(urls)
    # # print(text)
    # scraper._driver.close()
    # scraper._driver.quit()
