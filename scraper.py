import abc
from http.client import HTTPException
from typing import Union
import requests
import time
import os

from bs4 import BeautifulSoup

from model import Article, ArticleInfo
from errors import (
    ImageDownloadError,
    GetPageError,
    MajorError,
    MinorError,
    ImageSaveError,
)


class Scraper:
    __metaclass__ = abc.ABCMeta

    def __init__(self, article_infos: list[ArticleInfo], delay: int = None) -> None:
        self._article_infos = article_infos
        self._delay = delay

        if not os.path.exists("./images"):
            os.mkdir("./images")

    def _get_page_html(self, page_url: str) -> BeautifulSoup:
        try:
            res = requests.get(page_url)

            if res.status_code != 200:
                raise GetPageError(
                    f"Failed to request {page_url}. Moving on to the next page."
                )

            return BeautifulSoup(res.text, "html.parser")

        except GetPageError as e:
            raise e
        except Exception as e:
            raise MajorError(
                f"Something went wrong while getting page html of {page_url}: {str(e)}"
            )

    @abc.abstractmethod
    def _get_article_text(self, html: BeautifulSoup) -> str:
        pass

    @abc.abstractmethod
    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        pass

    @staticmethod
    def _make_directory_names(id: str, image_url: str) -> tuple[str, str]:
        image_foramt = image_url.split(".")[-1]
        image_name = str(i) + "." + image_foramt
        image_folder_directory = "./images/{}".format(id)
        image_directory = os.path.join(image_folder_directory, image_name)

        return (image_folder_directory, image_directory)

    @staticmethod
    def _make_image_request(image_url: str) -> requests.Response:
        image_request = requests.get(image_url)

        if image_request.status_code != 200:
            raise ImageDownloadError(f"Failed to save image(s) of {id}")

        return image_request

    @staticmethod
    def _save_image(image_directory: str, image_bytes: bytes) -> None:
        try:
            with open(image_directory, "wb") as f:
                f.write(image_bytes)
        except:
            raise ImageSaveError(
                f"Error occured while saving the image at {image_directory}"
            )

    def _save_images(self, id: str, image_urls: list[str]) -> list[str] | None:
        image_dirs = []

        for i, url in enumerate(image_urls):

            image_folder_directory, image_directory = self._make_directory_names(
                id, url
            )
            image_request = self._make_image_request(url)
            image_dirs.append(image_directory)
            os.mkdir(image_folder_directory)

            self._save_image(image_directory, image_request.content)

        if image_dirs:
            return image_dirs

    # 뉴스기사 내용 db에 저장
    def _save_article_content(self, article: Article) -> None:
        pass

    def _scrape_one_page(self, article_info: ArticleInfo) -> None:
        try:
            html = self._get_page_html(article_info.url)
            text = self._get_article_text(html)
            image_urls = self._get_article_image_urls(html)
            image_dirs = None
            if image_urls:
                image_dirs = self._save_images(article_info.id, image_urls)
            article = Article(text, image_dirs)
            self._save_article_content(article)
            if self._delay:
                time.sleep(self._delay)

        except MajorError as e:
            print(e)
            return
        except MinorError as e:
            print(e)
        except Exception as e:
            print(e)
            return

    def scrape(self):
        for url in self._article_infos:
            self._scrape_one_page(url)


class ChosunScraper(Scraper):
    def _get_article_text(self, html) -> str:
        return super()._get_article_text(html)

    def _get_article_image_urls(self, html) -> Union[list[str], str]:
        return super()._get_article_image_urls(html)

    def _save_article_content(self) -> None:
        return super()._save_article_content()

    def _scrape_one_page(self):
        return super()._scrape_one_page()
