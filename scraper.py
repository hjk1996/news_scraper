import abc
from http.client import HTTPException
from typing import Union
import requests
from bs4 import BeautifulSoup

class Scraper:
    __metaclass__ = abc.ABCMeta

    def __init__(self, urls: list[str]) -> None:
        self._urls = urls

    def _get_page_html(self, page_url: str):
        try:
            res = requests.get(page_url)

            if res.status_code != 200:
                raise HTTPException(
                    f"Failed to request {page_url}. Moving on to the next page."
                )

            html_text = res.text
            return BeautifulSoup(html_text, 'html.parser')

        except HTTPException as e:
            print(e)
        except Exception as e:
            print(e)

    @abc.abstractmethod
    def _get_article_text(
        self,
    ) -> str:
        pass

    @abc.abstractmethod
    def _get_article_image_urls(
        self,
    ) -> Union[list[str], str]:
        pass

    # 뉴스기사 내용 db에 저장
    @abc.abstractclassmethod
    def _save_article_content(
        self,
    ) -> None:
        pass

    @abc.abstractmethod
    def scrape(self):
        pass
