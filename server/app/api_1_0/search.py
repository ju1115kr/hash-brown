# -*- coding:utf-8 -*-
from flask import request, jsonify, g
from . import api
from .authentication import auth
from ..models import News, User
from .errors import not_found, forbidden, bad_request
from datetime import datetime


@api.route('/search/news/<context>', methods=['GET'])
@auth.login_required
def search_news(context):
    if context is None:
        return bad_request('Request is invaild')

    context = context.lower()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 60, type=int)
    pagination = News.query\
                    .filter(News.parsed_context.like('%'+context+'%'))\
                    .order_by(News.id.desc())\
                    .paginate(page, per_page, error_out=False)
    pag_result = pagination.items
	
    if pagination is None:
        return not_found('Result does not exist')
    return jsonify({'news':[news.to_json() for news in pag_result]})

