from scraper_abc import Scraper
from bs4 import BeautifulSoup


class DongAScraper(Scraper):
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

    # TO-DO: xpath로 이미지 검색이 안됨. 이거 해결해야함.
    def _get_article_text(self, html: BeautifulSoup) -> str:
        html.find("div", "article_footer").decompose()
        article = html.find("div", "article_txt")
        return article.text.replace("\n", "")
