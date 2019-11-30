from app.libs.httper import HTTP
from flask import current_app


class YuShuBook:
    per_page = 15
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def search_by_keyword(self, keyword, page):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], cls.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_collection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    def calculate_start(self, page):
        return current_app.config['PER_PAGE'] * (page - 1)
