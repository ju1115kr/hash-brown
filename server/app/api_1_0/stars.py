# -*- coding:utf-8 -*-
from  flask import request, jsonify, make_response, url_for, g
from . import api
from .authentication import auth
from .. import db
from ..models import User, News, Star
from .errors import not_found, forbidden, bad_request
from datetime import datetime
from flask_cors import cross_origin
import os


@api.route('/news/<int:id>/star', methods=['POST'])
@auth.login_required
@cross_origin(expose_headers='Location')
def post_news_star(id):
    news = News.query.get(id)
    if news is None:
        return not_found('News does not exist')

    if int(g.current_user.id) in [star.user_id for star in news.stars]:
        return bad_request('user already stared this news')

    star = Star(user_id=g.current_user.id, news_id=id)
    db.session.add(star)
    db.session.commit()

    return jsonify(news.to_json())


@api.route('/news/<int:id>/star', methods=['DELETE'])
@auth.login_required
def delete_news_star(id):
    news = News.query.get(id)
    if news is None:
        return not_found('News does not exist')

    if int(g.current_user.id) not in [star.user_id for star in news.stars]:
        return bad_request('user does not stared this news')

    star = Star.query.filter_by(user_id=g.current_user.id) \
            .filter_by(news_id=id).first()

    db.session.delete(star)
    db.session.commit()

    return '', 204
