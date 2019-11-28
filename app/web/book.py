from flask import jsonify, request

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key

from app.spider.yushu_book import YuShuBook
from . import web


@web.route('/book/search/<q>/<page>')
def search(q, page):
    """
        q:普通关键、isbn
        page
    :return:
    """

    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        is_or_key = is_isbn_or_key(q)
        if is_or_key == 'isbn':
            result = YuShuBook.search_by_isbn(q)

        else:
            result = YuShuBook.search_by_keyword(q,page)

        return jsonify(result)

    else:
        return jsonify(form.errors)


@web.route('/book/test')
def test():
    return jsonify({})
