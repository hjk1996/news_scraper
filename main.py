from scraper import *
from scraper_abc import Scraper
import sqlite3
from glob import glob
from util import make_chrome_driver


def test_get_article_image_urls_method(scraper: Scraper, url: str) -> None:
    html = scraper._get_html_method(url)
    image_urls = scraper._get_article_image_urls(html)

    if not image_urls:
        print("Failed to retrieve image urls from html")
    else:
        print(image_urls)


def test_get_article_text_method(scraper: Scraper, url: str) -> None:
    html = scraper._get_html_method(url)
    text = scraper._get_article_text(html)
    print(text)


if __name__ == "__main__":

    con = sqlite3.connect("./news.db")
    cursor = con.cursor()

    driver = None

    # driver = make_chrome_driver()
    url = "https://www.ytn.co.kr/_ln/0101_202205312147243645"
    scraper = YTNScraper(cursor)
    # scraper.scrape()

    test_get_article_image_urls_method(scraper, url)
    test_get_article_text_method(scraper, url)

    if driver:
        driver.close()
        driver.quit()
