# -*- coding: utf-8 -*-
from flask import current_app, make_response, request, url_for, g, jsonify, send_from_directory
from . import api
from .authentication import auth
from .. import db
from ..models import User, News
from .errors import not_found, forbidden, bad_request
from werkzeug import secure_filename
import web3
from web3 import Web3, HTTPProvider
from web3.auto import w3


@api.route('/users', methods=['POST'])
def post_user():
    user = User.from_json(request.json)
    web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    coinbase = w3.eth.coinbase
    user.ethereum_id = web3.personal.newAccount(user.password_hash)
    web3.personal.unlockAccount(user.ethereum_id, user.password_hash)

    db.session.add(user)
    db.session.commit()
    resp = make_response()
    resp.headers['Location'] = url_for('api.get_user', user_id=user.username)
    resp.status_code = 201
    return resp


@api.route('/users/<user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = User.query.filter_by(username=user_id).first()
    if user is None:
        return not_found('User does not exist')
    return jsonify(user.to_json())


@api.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    users = User.query.all()
    return jsonify({
        'users': [user.to_json() for user in users]
    }), 200


@api.route('/users/<user_id>', methods=['PUT'])
@auth.login_required
def modify_user(user_id):
    user = User.query.filter_by(username=user_id).first()
    if user is None:  # 유저가 존재 하지 않을 경우
        return not_found('User does not exist')
    if g.current_user.username is not user.username:  # 다른 유저를 수정하려고 하는 경우
        return forbidden('Cannot modify other user')
    if request.json is None:  # 요청이 올바르지 않은 경우
        return bad_request('JSON Request is invaild')
    if request.json.get('pw') is not None:  # pw 를 수정하는 경우
        user.password = request.json.get('pw')
    user.realname = request.json.get('name', user.realname)
    db.session.add(user)
    return jsonify(user.to_json())


@api.route('/users/<user_id>/news', methods=['GET'])
@auth.login_required
def get_user_news(user_id):
    user = User.query.filter_by(username=user_id).first()
    if user is None:
        return not_found('User does not exist')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    pagination = user.news.order_by(News.created_at.desc()).paginate(page, per_page, error_out=False)
    pag_news = pagination.items
    if pagination.total < 1:
        return not_found('User does not have news')
    return jsonify({'news': [news.to_json() for news in pag_news]})

