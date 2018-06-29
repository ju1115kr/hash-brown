# -*- coding:utf-8 -*-
from flask import request, jsonify, make_response, url_for, g
from . import api
from .authentication import auth
from .. import db
from ..models import User, News
from .errors import not_found, forbidden, bad_request
from datetime import datetime
from flask_cors import cross_origin
import os


@api.route('/news', methods=['GET'])
@auth.login_required
def get_all_news():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    pagination = News.query.order_by(News.created_at.desc()).paginate(page, per_page, error_out=False)
    pag_news = pagination.items
    return jsonify({'news': [news.to_json() for news in pag_news]})


@api.route('/news/<int:id>', methods=['GET'])
@auth.login_required
def get_news(id):
    news = News.query.get(id)
    if news is None:
        return not_found('News does not exist')
    return jsonify(news.to_json())


@api.route('/news', methods=['POST'])
@auth.login_required
@cross_origin(expose_headers='Location')
def post_news():
    if request.json is None:
        return bad_request('JSON Request is invaild')
    news = News.from_json(request.json)
    news.author_id = g.current_user.id

    db.session.add(news)
    db.session.commit()
    resp = make_response()
    resp.headers['Location'] = url_for('api.get_news', id=news.id)
    resp.status_code = 201
    return resp


@api.route('/news/<int:news_id>', methods=['PUT'])
@auth.login_required
def put_news(news_id):
    if request.json is None:
        return bad_request('JSON Request is invaild')
    old_news = News.query.filter_by(id=news_id).first()
    if old_news is None:
        return not_found('News does not exist')
    if g.current_user.id != old_news.author_id:
        return forbidden('Cannot modify other user\'s news')  
    news = News.from_json(request.json)
    old_news.context = news.context
    old_news.parsed_context = news.parsed_context
    old_news.modified_at = datetime.utcnow()
    return jsonify(old_news.to_json())


@api.route('/news/<int:news_id>', methods=['DELETE'])
@auth.login_required
def delete_news(news_id):
    news = News.query.filter_by(id=news_id).first()
    if news is None:
        return not_found('News does not exist')
    if g.current_user.id != news.author_id:
        return forbidden('Cannot delete other user\'s news')
    Comment.query.filter(Comment.news_id == news.id).delete()
    db.session.delete(news)
    db.session.commit()
    return '', 204



@api.route('/news/<int:news_id>/associate', methods=['GET'])
@auth.login_required
def get_news_associate(news_id):
    news = News.query.get(news_id)
    if news is None:
        return not_found('News does not exist')
    return jsonify({'news': [each_news.to_json() for each_news in news.associated if each_news.parent_id is news_id]})


@api.route('/news/<int:news_id>/associate', methods=['POST'])
@auth.login_required
@cross_origin(expose_headers='Location')
def post_news_associate(news_id):
    if request.json is None:
        return bad_request('JSON Request is invaild')
    parent_news = News.query.get(news_id)
    if parent_news is None:
        return not_found('news does not exist')

    news = News.from_json(request.json)
    news.author_id = g.current_user.id
    news.parent_id = news_id
    news.refutation = request.json.get('refutation')

    db.session.add(news)
    db.session.commit()
    resp = make_response()
    resp.headers['Location'] = url_for('api.get_news', id=news.id)
    resp.status_code = 201
    return resp

