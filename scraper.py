import re

from scraper_abc import Scraper
from bs4 import BeautifulSoup
import bs4
from sqlite3 import Cursor
from selenium import webdriver

from errors import NoDriverError, NotAllowedUrlFormatError

# 드라이버 필요함
class ChosunScraper(Scraper):
    def __init__(
        self, db_curosr: Cursor, delay: int = None, driver: webdriver.Chrome = None
    ) -> None:
        super().__init__(db_curosr, delay, driver)

        if driver == None:
            raise NoDriverError(f"{self.__class__.__name__} needs a webdriver.")

    @property
    def press(self) -> str:
        return "조선일보"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("section", "article-body")
        photos: list[bs4.element.Tag] = article.find_all("img")
        for photo in photos:
            image_urls.append(photo["src"])

        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        text = ""
        article = html.find("section", "article-body")
        paragraphs: list[bs4.element.Tag] = article.find_all("p")
        for paragraph in paragraphs:
            text += paragraph.text

        return " ".join(text.split())


class DongaScraper(Scraper):
    @property
    def press(self) -> str:
        return "동아일보"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", "article_txt")
        photos: list[bs4.element.Tag] = article.find_all("div", "articlePhotoC")
        for photo in photos:
            image_url = photo.find("img")["src"]

            image_urls.append(image_url)

        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        article = html.find("div", "article_txt")
        article.find("div", "article_footer").decompose()
        text = " ".join(article.text.split())
        return text


class ChoongangScraper(Scraper):
    @property
    def press(self) -> str:
        return "중앙일보"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", "article_body fs3")
        photos: list[bs4.element.Tag] = article.find_all("div", "ab_photo photo_center")
        for photo in photos:
            image_url = photo.find("img", recursive=True)["src"].replace("/_ir50_/", "")
            image_urls.append(image_url)
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        text = ""
        article = html.find("div", "article_body fs3")

        paragraphs: list[bs4.element.Tag] = article.find_all("p")
        for paragraph in paragraphs:
            text += paragraph.text

        return " ".join(text.split())


class HankookScraper(Scraper):
    @property
    def press(self) -> str:
        return "한국일보"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"itemprop": "articleBody"})
        photos: list[bs4.element.Tag] = article.find_all("div", "editor-img-box")
        for photo in photos:
            image_url = photo.find("img")["src"]

            image_urls.append(image_url)
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        text = ""
        article = html.find("div", attrs={"itemprop": "articleBody"})
        paragraphs: list[bs4.element.Tag] = article.find_all("p", "editor-p")
        for p in paragraphs:
            text += p.text

        return " ".join(text.split())


class HankyorehScraper(Scraper):
    @property
    def press(self) -> str:
        return "한겨레"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", "article-text").find("div", "text")
        photos: list[bs4.element.Tag] = article.find_all("div", "image")
        for photo in photos:
            image_url = photo.find("img")["src"]
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            image_urls.append(image_url)
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        article = html.find("div", "article-text").find("div", "text")
        text = " ".join(article.text.split())
        return text


# 드라이버 필요함
class KyunghyangScraper(Scraper):
    def __init__(
        self, db_curosr: Cursor, delay: int = None, driver: webdriver.Chrome = None
    ) -> None:
        super().__init__(db_curosr, delay, driver)

        if driver == None:
            raise NoDriverError(f"{self.__class__.__name__} needs a webdriver.")

    @property
    def press(self) -> str:
        return "경향신문"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", "art_body")
        photos: list[bs4.element.Tag] = article.find_all("img")
        for photo in photos:
            image_url = photo["src"]
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            image_urls.append(image_url)
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        text = ""
        article = html.find("div", "art_body")
        paragraphs: list[bs4.element.Tag] = article.find_all("p", "content_text")
        for paragraph in paragraphs:
            text += paragraph.text

        return " ".join(text.split())


class KookminScraper(Scraper):
    @property
    def press(self) -> str:
        return "국민일보"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"id": "articleBody"})
        figures: list[bs4.element.Tag] = article.find_all("figure")
        for figure in figures:
            photo = figure.find("img")
            image_urls.append(photo["src"])
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        article = html.find("div", attrs={"id": "articleBody"})

        subscribe = article.find("div", attrs={"class": "ms_subscribe"})

        if subscribe:
            subscribe.decompose()

        text = " ".join(article.text.split())
        return text


class MaeilKyungjeScraper(Scraper):
    @property
    def press(self) -> str:
        return "매일경제"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"id": "article_body"})
        photos: list[bs4.element.Tag] = article.find_all("img")
        for photo in photos:
            if photo["src"].startswith("https"):
                image_urls.append(photo["src"])
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        article = html.find("div", attrs={"id": "article_body"})
        article.find("figure").decompose()
        article.find("div", "zoom_txt").decompose()
        text = " ".join(article.find("div", "art_txt").text.split())
        return text


class NaeilScraper(Scraper):
    @property
    def press(self) -> str:
        return "내일신문"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", "article")
        photos: list[bs4.element.Tag] = article.find_all("img")
        for photo in photos:
            image_urls.append(photo["src"])
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        text = ""
        article = html.find("div", "article")
        paragraphs: list[bs4.element.Tag] = article.find_all("p")

        for paragraph in paragraphs:
            text += paragraph.text

        return " ".join(text.split())


class MunhwaScraper(Scraper):
    @property
    def press(self) -> str:
        return "문화일보"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"id": "NewsAdContent"})
        photos: list[bs4.element.Tag] = article.find_all("img")
        for photo in photos:
            image_url = "".join(photo["src"].split("?")[:-1])
            image_urls.append(image_url)
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        article = html.find("div", attrs={"id": "NewsAdContent"})
        text = " ".join(article.text.split())
        return text


class SeoulScraper(Scraper):
    def __init__(
        self, db_curosr: Cursor, delay: int = None, driver: webdriver.Chrome = None
    ) -> None:
        super().__init__(db_curosr, delay, driver)
        self._article_infos = [
            article_info
            for article_info in self._article_infos
            if "www.seoul.co.kr" in article_info.url
        ]

    @property
    def press(self) -> str:
        return "서울신문"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"itemprop": "articleBody"})
        photos: list[bs4.element.Tag] = article.find_all("img")
        for photo in photos:
            image_url = photo["src"]
            if image_url.startswith("//"):
                image_url = "https:" + image_url
                image_urls.append(image_url)
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        article = html.find("div", attrs={"itemprop": "articleBody"})
        text = " ".join(article.text.split())
        return text


class SegyeScraper(Scraper):
    @property
    def press(self) -> str:
        return "세계일보"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"itemprop": "articleBody"})
        photos: list[bs4.element.Tag] = article.find_all("img")
        for photo in photos:
            image_url = photo["src"]
            if image_url.startswith("//"):
                image_url = "https:" + image_url
                image_urls.append(image_url)
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        text = ""
        article = html.find("div", attrs={"itemprop": "articleBody"})
        paragraphs: list[bs4.element.Tag] = article.find_all("p")
        for p in paragraphs:
            text += p.text
        text = " ".join(text.split())
        text = text.replace("[ⓒ 세계일보 & Segye.com, 무단전재 및 재배포 금지]", "")
        return text


class MaekyungScraper(Scraper):
    def __init__(
        self, db_curosr: Cursor, delay: int = None, driver: webdriver.Chrome = None
    ) -> None:
        super().__init__(db_curosr, delay, driver)

        self._article_infos = [
            article_info
            for article_info in self._article_infos
            if "news.mk.co.kr" in article_info.url
        ]

    @property
    def press(self) -> str:
        return "매일경제"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"itemprop": "articleBody"}).find('div', 'art_txt')
        photos: list[bs4.element.Tag] = article.find_all("img")
        for photo in photos:
            image_urls.append(photo['src'])
        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        article = html.find("div", attrs={"itemprop": "articleBody"}).find('div', 'art_txt')
        text = " ".join(article.text.split()) 
        text = text.replace("[ⓒ 매일경제 & mk.co.kr, 무단전재 및 재배포 금지]", "")
        return text

class MoneyTodayScraper(Scraper):
    
    @property
    def press(self) -> str:
        return "머니투데이"

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"itemprop": "articleBody"})
        photos: list[bs4.element.Tag] = article.find_all("img")
        for photo in photos:
            image_url = photo['src']
            
            if image_url.startswith('//'):
                image_url = 'https:' + image_url

            if image_url.endswith('/dims/optimize'):
                image_url = image_url.replace('/dims/optimize', '')
            
            image_urls.append(image_url)

        return image_urls

    def _get_article_text(self, html: BeautifulSoup) -> str:
        article = html.find("div", attrs={"itemprop": "articleBody"})
        text = " ".join(article.text.split()) 
        return text

class SeoulKyungjeScraper(Scraper):
    
    @property
    def press(self) -> str:
        return "서울경제"
    
    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"itemprop": "articleBody"})
        photos: list[bs4.element.Tag] = article.find_all('img')
        for photo in photos:
            image_urls.append(photo['src'])
        return image_urls
    
    def _get_article_text(self, html: BeautifulSoup) -> str:
        article = html.find("div", attrs={"itemprop": "articleBody"})

        article_copy = article.find('div', 'article_copy')

        if article_copy:
            article_copy.decompose()

        text = " ".join(article.text.split())

        if text.startswith('viewer '):
            text = text.replace('viewer ', '')

        return text 

class AsiaKyungjeScraper(Scraper):

    @property
    def press(self) -> str:
        return '아시아경제'

    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        image_urls = []
        article = html.find("div", attrs={"itemprop": "articleBody"})
        photos: list[bs4.element.Tag] = article.find_all('img')
        for photo in photos:
            image_urls.append(photo['src'])
        return image_urls
    
    def _get_article_text(self, html: BeautifulSoup) -> str:
        text = ''
        article = html.find("div", attrs={"itemprop": "articleBody"})

        im_re_box = article.find('div', 'im_re_box')
        if im_re_box:
            im_re_box.decompose()
        
        txt_prohibition = article.find('p', 'txt_prohibition')
        if txt_prohibition:
            txt_prohibition.decompose()

        paragraphs: list[bs4.element.Tag] = article.find_all("p")
        for p in paragraphs:
            text += p.text
        
        text = ' '.join(text.split())

        if re.match(r'\[아시아경제.*\]', text):
            text = re.sub(r'\[아시아경제.*\]', '', text).strip()

        return text
