from numpy import choose
from scraper import (
    DongaScraper,
    ChoongangScraper,
    KyunghyangScraper,
    HankyorehScraper,
    ChosunScraper,
    HankookScraper,
    MaeilScraper
)
import sqlite3
from glob import glob


if __name__ == "__main__":

    con = sqlite3.connect("./news.db")
    cursor = con.cursor()

    scraper = MaeilScraper(cursor)
    scraper.scrape()
    # html = scraper._get_html_method("https://www.mk.co.kr/news/society/view/2022/07/582827/")
    # image_urls = scraper._get_article_image_urls(html)
    # text = scraper._get_article_text(html)
    # print(text)


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

    # scraper = HankyorehScraper(cursor)
    # scraper.scrape()
    # html = scraper._get_html_method("https://www.hani.co.kr/arti/society/society_general/1050355.html")
    # urls = scraper._get_article_image_urls(html)
    # text = scraper._get_article_text(html)
    # print(urls)
    # print(text)

    # scraper = ChosunScraper(cursor, need_driver=True)
    # scraper.scrape()
    # html = scraper._get_html_method("https://www.chosun.com/politics/politics_general/2022/07/11/PZ42VU4TZNEFDPVNUQ2DM7VXPA/")
    # urls = scraper._get_article_image_urls(html)
    # text = scraper._get_article_text(html)
    # print(urls)
    # print(text)

    # scraper._driver.close()
    # scraper._driver.quit()

    # scraper = HankookScraper(cursor)
    # html = scraper._get_html_method(
    #     "https://www.hankookilbo.com/News/Read/A2022071111190004907"
    # )
    # # print(html.find("div", attrs= {"itemprop": "articleBody"}))
    # urls = scraper._get_article_image_urls(html)
    # text = scraper._get_article_text(html)
    # print(urls)
    # print(text)
