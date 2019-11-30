from flask import request, jsonify, flash, render_template

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
import json

from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel, BookCollection
from . import web


@web.route('/book/search')
def search():
    """
        q:普通关键、isbn
        page
    :return:
    """
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        is_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if is_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)

        # return json.dumps(books, default=lambda x: x.__dict__)
        # return jsonify(books)

    else:
        flash('搜索关键字不符合要求，请重新输入关键字')

    return render_template('search_result.html', books=books)
