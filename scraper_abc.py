import abc
import re
from sqlite3 import Cursor

from webbrowser import Chrome
import requests
import time
import os
import pandas as pd
import pickle


from selenium import webdriver


from bs4 import BeautifulSoup

from model import ArticleInfo
from errors import (
    ImageDownloadError,
    GetPageError,
    MajorError,
    MinorError,
    ImageSaveError,
    SaveError,
)


class Scraper:
    __metaclass__ = abc.ABCMeta

    def __init__(
        self, db_curosr: Cursor, delay: int = None, driver: webdriver.Chrome = None
    ) -> None:
        self._delay = delay
        self._cursor = db_curosr
        self._driver = driver
        self._get_html_method = (
            self._get_page_html_from_driver if driver != None else self._get_page_html
        )
        self._saving_list = []

        self._image_folder_dir = f"./images/{self.press}"

        os.makedirs(self._image_folder_dir, exist_ok=True)
        os.makedirs('./data', exist_ok=True)



        self._load_data_from_db()

    @property
    def need_driver() -> bool:
        return False

    @property
    @abc.abstractmethod
    def press(self) -> str:
        pass

    def _load_data_from_db(self):
        try:
            self._cursor.execute("SELECT * FROM news WHERE press =?", (self.press,))
            article_infos = self._cursor.fetchall()
            self._article_infos = self._convert_to_article_info_object(article_infos)
        except Exception as e:
            print("Failed to load data from db")
            raise e

    @staticmethod
    def _convert_to_article_info_object(
        article_infos: list[list[str]],
    ) -> list[ArticleInfo]:
        return [ArticleInfo(*info) for info in article_infos]

    def _get_page_html(self, page_url: str) -> BeautifulSoup:
        try:

            res = requests.get(page_url)

            if res.status_code != 200:
                raise GetPageError(
                    f"Failed to request {page_url}. Moving on to the next page."
                )

            return BeautifulSoup(res.content, "html.parser")

        except GetPageError as e:
            raise e
        except Exception as e:
            raise MajorError(
                f"Something went wrong while getting page html of {page_url}: {str(e)}"
            )

    def _get_page_html_from_driver(self, page_url: str) -> BeautifulSoup:
        self._driver.get(page_url)
        page_source = self._driver.page_source
        return BeautifulSoup(page_source, "html.parser")

    @abc.abstractmethod
    def _get_article_text(self, html: BeautifulSoup) -> str:
        pass

    @abc.abstractmethod
    def _get_article_image_urls(self, html: BeautifulSoup) -> list[str] | None:
        pass

    @staticmethod
    def _make_image_request(id: str, image_url: str) -> requests.Response:
        image_request = requests.get(image_url)

        if image_request.status_code != 200:
            raise ImageDownloadError(f"Failed to save image(s) of {id}")

        return image_request

    @staticmethod
    def _save_image(image_path: str, image_bytes: bytes) -> None:
        try:
            with open(image_path, "wb") as f:
                f.write(image_bytes)
        except:
            raise ImageSaveError(
                f"Error occured while saving the image at {image_path}"
            )

    def _save_images(self, id: str, image_urls: list[str]) -> list[str] | None:
        image_paths = []

        image_folder_directory = self._image_folder_dir + f'/{id}'
        os.makedirs(image_folder_directory, exist_ok=True)
        for order, url in enumerate(image_urls):
            image_name = f"{order}.{url.split('.')[-1]}"
            image_path = os.path.join(image_folder_directory, image_name)
            image_request = self._make_image_request(id, url)
            image_paths.append(image_path)
            self._save_image(image_path, image_request.content)

        if image_paths:
            return image_paths

    # ???????????? ?????? db??? ??????
    def _save_data(self) -> None:

        try:
            with open(f"./data/{self.press}.pickle", "wb") as file:
                pickle.dump(self._saving_list, file, pickle.HIGHEST_PROTOCOL)

        except Exception as e:
            raise SaveError("Failed to save the data")

    @staticmethod
    def _remove_unnecessary_white_space(text: str) -> str:
        return " ".join(text.split())

    @staticmethod
    def _remove_not_korean(text: str) -> str:
        korean = re.compile(r"[^ ???-??????-???+]")
        return korean.sub(" ", text)

    @staticmethod
    def _remove_reporter_name(text: str) -> str:
        return re.sub(r"[???-??????-???]+ ??????", "", text)

    def _scrape_one_page(self, article_info: ArticleInfo) -> None:
        try:
            html = self._get_html_method(article_info.url)
            text = self._get_article_text(html)
            image_urls = self._get_article_image_urls(html)
            image_dirs = None
            if image_urls:
                image_dirs = self._save_images(article_info.hash_id, image_urls)

            article_info.set_values(text, image_dirs)
            self._saving_list.append(article_info)
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

        self._save_data()
