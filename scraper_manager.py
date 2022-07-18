
from scraper_abc import Scraper
import scraper
import sqlite3
from util import make_chrome_driver


class ScraperManager:
    def __init__(self) -> None:
        self._cursor = sqlite3.connect("./news.db").cursor()
        self._scraper_classes = [
            scraper.AjuKyungjeScraper,
            scraper.AsiaKyungjeScraper,
            scraper.ChoongangScraper,
            scraper.ChosunScraper,
            scraper.DongaScraper,
            scraper.FinancialNewsScraper,
            scraper.HankookScraper,
            scraper.HankyorehScraper,
            scraper.HankyungScraper,
            scraper.HeraldKyungjeScraper,
            # scraper.KBSScraper,
            scraper.KookminScraper,
            scraper.KyunghyangScraper,
            scraper.MaeilKyungjeScraper,
            # scraper.MBCScraper,
            scraper.MoneyTodayScraper,
            scraper.MunhwaScraper,
            scraper.NaeilScraper,
            # scraper.OBSScraper,
            # scraper.SBSScraper,
            scraper.SegyeScraper,
            scraper.SeoulKyungjeScraper,
            scraper.SeoulScraper,
            # scraper.YTNScraper,
        ]

        self._scrapers = []

    def scrape_all(self) -> None:
        
        for scraper_class in self._scraper_classes:
            if scraper_class.need_driver:
                driver = make_chrome_driver()
            worker: Scraper = scraper_class(self._cursor, driver=driver) if scraper_class.need_driver else scraper_class(self._cursor,)
            worker.scrape()

            if scraper_class.need_driver:
                driver.close()
                driver.quit()
        
