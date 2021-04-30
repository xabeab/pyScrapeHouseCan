import requests
from bs4 import BeautifulSoup


class Ad:

    def __init__(self, url: str):
        self.url = url

        lst_url = url.split('/')

        self.category = lst_url[3]
        self.location = lst_url[4]
        self.title = lst_url[5]
        self.id = int(lst_url[6])

        self.soup = None

    """
    Methods that extracts from soups the elements needed
    """
    def parse_with_soup(self) -> None:
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, 'html5lib')

    def print_attributes(self) -> None:

        print(self.url)
        print()
        print(self.title)
        print()
        print(self.id)
        print()
