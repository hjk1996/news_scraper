from numpy import choose
from scraper import DongAScraper, ChoongAngScraper, KyunghyangScraper, HankyorehScraper
import sqlite3
from glob import glob


if __name__ == "__main__":

    con = sqlite3.connect("./news.db")
    cursor = con.cursor()

    # scraper = DongAScraper(cursor)
    # scraper.scrape()

    # scraper = ChoongAngScraper(cursor)
    # scraper.scrape()

    # scraper = KyunghyangScraper(cursor, need_driver=True)
    # scraper.scrape()
    # html = scraper._get_page_html_from_driver(
    #     "https://www.khan.co.kr/national/court-law/article/202207101908001"
    # )
    # urls = scraper._get_article_image_urls(html)
    # text = scraper._get_article_text(html)
    # print(urls)
    # # print(text)
    # scraper._driver.close()
    # scraper._driver.quit()
    
    scraper = HankyorehScraper(cursor)
    scraper.scrape()
    # html = scraper._get_html_method("https://www.hani.co.kr/arti/society/society_general/1050355.html")
    # urls = scraper._get_article_image_urls(html)
    # text = scraper._get_article_text(html)
    # print(urls)
    # print(text)