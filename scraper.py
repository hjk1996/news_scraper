from scraper_abc import Scraper
from bs4 import BeautifulSoup
import bs4


class ChosunScraper(Scraper):
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
        texts = []
        article = html.find("section", "article-body")
        paragraphs: list[bs4.element.Tag] = article.find_all("p")
        for paragraph in paragraphs:
            texts.append(paragraph.text.strip())

        return " ".join(texts)


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
        html.find("div", "article_footer").decompose()
        article = html.find("div", "article_txt")
        return article.text.replace("\n", "")


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
        texts = []
        article = html.find("div", "article_body fs3")

        paragraphs: list[bs4.element.Tag] = article.find_all("p")
        for paragraph in paragraphs:
            texts.append(paragraph.text.strip())

        return " ".join(texts)


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
        texts = []
        article = html.find("div", attrs={"itemprop": "articleBody"})
        paragraphs: list[bs4.element.Tag] = article.find_all("p", "editor-p")
        for p in paragraphs:
            text = p.text.strip()
            texts.append(text)

        return " ".join(texts)


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
        text = article.text.strip().replace("\n", "")
        return text


class KyunghyangScraper(Scraper):
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
        texts = []
        article = html.find("div", "art_body")
        paragraphs: list[bs4.element.Tag] = article.find_all("p", "content_text")
        for paragraph in paragraphs:
            texts.append(paragraph.text.strip())

        return " ".join(texts)
