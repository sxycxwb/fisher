class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.pages = book['pages']


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, book, keyword):
        self.total = book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in book.books]


class _BookViewModel:

    def package_single(self, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['data'] = [self.__cut_book_data(data)]
        return returned

    def package_collection(self, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['data'] = [self.__cut_book_data(book) for book in data['books']]
        return returned

    def __cut_book_data(self, data):
        book = {
            'title': data['data'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image'],
            'author': '、'.join(data['author'])
        }
        return book
