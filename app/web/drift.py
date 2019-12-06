from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc, or_

from app import db
from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web

__author__ = 'summer'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash("这本书是你自己的，不能向自己所要书籍")
        return redirect(url_for(web.book_detail, isbn=current_gift.isbn))
    can_send = current_user.can_send_drift()
    if not can_send:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        # 发邮件
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html', wisher=current_user)

    gifter = current_gift.user.summary()
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(or_(
        Drift.requester_id == current_user.id,
        Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.fiter(Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Redraw


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # drift.message = drift_form.message.data
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_id = current_gift.user.id
        drift.gifter_nickname = current_user.user.nickname

        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.save(drift)
