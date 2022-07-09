import abc
from http.client import HTTPException
from sqlite3 import Cursor
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
    DBSaveError
)


class Scraper:
    __metaclass__ = abc.ABCMeta
    

    def __init__(
        self, db_cursor: Cursor, delay: int = None
    ) -> None:
        self._cursor = db_cursor
        self._delay = delay

        self._load_data_from_db()
        
        if not os.path.exists("./images"):
            os.mkdir("./images")

    @property
    @abc.abstractmethod
    def press(self) -> str:
        pass

    def _load_data_from_db(self):
        try:
            self._cursor.execute("SELECT * FROM news WHERE press =?", (self.press, ))
            article_infos =  self._cursor.fetchall()
            self._article_infos = self._convert_to_article_info_object(article_infos)
            print(len(self._article_infos))
        except Exception as e:
            print("Failed to load data from db")
            raise e

    @staticmethod
    def _convert_to_article_info_object(article_infos: list[list[str]]) -> list[ArticleInfo]:
        return [ArticleInfo(*info) for info in article_infos]


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
    def _make_directory_names(id: str, order: int, image_url: str) -> tuple[str, str]:
        image_foramt = image_url.split(".")[-1]
        image_name = str(order) + "." + image_foramt
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

        for order, url in enumerate(image_urls):

            image_folder_directory, image_directory = self._make_directory_names(
                id, order, url
            )
            image_request = self._make_image_request(url)
            image_dirs.append(image_directory)
            os.mkdir(image_folder_directory)

            self._save_image(image_directory, image_request.content)

        if image_dirs:
            return image_dirs

    # 뉴스기사 내용 db에 저장
    def _save_content(self, article: Article) -> None:
        try:
            self._cursor.execute(
                "UPDATE news SET content = ? image_urls = ? WHERE id = ?",
                (article.text, article.image_dirs, article.id),
            )
        except Exception as e:
            raise DBSaveError(f"Error occured while saving {article.id} in database")
            

    def _scrape_one_page(self, article_info: ArticleInfo) -> None:
        try:
            html = self._get_page_html(article_info.url)
            text = self._get_article_text(html)
            image_urls = self._get_article_image_urls(html)
            image_dirs = None
            if image_urls:
                image_dirs = self._save_images(article_info.id, image_urls)
            article = Article(article_info.id, text, image_dirs)
            self._save_content(article)
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
    
    @property
    def press(self) -> str:
        return "조선일보"
