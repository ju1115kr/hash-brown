# -*- coding: utf-8 -*-
from flask import url_for, current_app, g
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db
from app.exceptions import ValidationError
from datetime import datetime 


# 유저-뉴스 간 Many-to-Many 관계 테이블
class Star(db.Model):
    __tablename__ = 'stars'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'),
                        primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    ethereum_id = db.Column(db.Text)
    realname = db.Column(db.Text)
    password_hash = db.Column(db.String(128))
    tier = db.Column(db.Integer)
    balance = db.Column(db.Integer)

    stars = db.relationship('Star',
                    foreign_keys=[Star.user_id],
                    backref=db.backref('user', lazy='joined'),
                    lazy='dynamic',
                    cascade='all, delete-orphan')

    news = db.relationship('News', backref='author', lazy='dynamic')

    def __init__(self, username, realname, password):
        self.username = username
        self.realname = realname
        self.password = password
        self.balance = 0
        self.tier = ''

    def __repr__(self):
        return '<User %r[%r]>' % (self.username, self.realname)
    
    @property
    def password(self):  # password 맴버 변수 직접 접근 차단
        raise AttributeError('password is not a readable attrubute')

    @property
    def is_authenticated(self):
        return True

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])
        
    def to_json(self):  # json 출력 루틴
        json_user = {
            'id': self.id,
            'username': self.username,
            'realname': self.realname,
            'ethereum_id': self.ethereum_id,
            'tier': self.tier,
            'balance': self.balance,
            'stars': [ star.id for star in self.stars ],
            'starcount': self.stars.count(),
        }
        return json_user
    
    @staticmethod
    def from_json(json_user):  # json 입력 루틴
        user_id = json_user.get('id')
        user_pw = json_user.get('pw')
        user_name = json_user.get('name')
	        
        if user_id is None or user_id == '':
            raise ValidationError('user does not have a id')
        elif user_pw is None or user_pw == '':
            raise ValidationError('user does not have a pw')
        elif user_name is None or user_name == '':
            raise ValidationError('user does not have a name')
        
        return User(username=user_id, realname=user_name, password=user_pw)


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    context = db.Column(db.Text, nullable=False)
    parsed_context = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True,
                    default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    associated = db.relationship('News', lazy='dynamic')
    refutation = db.Column(db.Boolean)

    stars = db.relationship('Star',
                    foreign_keys=[Star.news_id],
                    backref=db.backref('news', lazy='joined'),
                    lazy='dynamic',
                    cascade='all, delete-orphan') 

    def __init__(self, context, parsed_context, author=None, refutation=False):
        self.context = context
        self.parsed_context = parsed_context
        self.refutation = refutation
        if author is not None:
            self.author_name = author.realname
            self.author = author

    def __repr__(self):
        return '<News [%r](%r):%r>' % (self.created_at, self.author_id, self.context)

    def to_json(self):  # json 출력 루틴
        json_news = {
            'id': self.id,
            'author': self.author.username,
            'author_name': self.author.realname,
            'context': self.context,
            'created_at': self.created_at,
            'parent_id': self.parent_id,
	    'refutation': self.refutation,
            'stars': [ star.username for star in self.stars ],
            'associated_reply': self.associated.count()
        }
        return json_news

    @staticmethod
    def from_json(json_news):  # json 입력 루틴
        context = json_news.get('context')
        if context is None or context == '':
            raise ValidationError('news does not have a context')
        parsed_context = removeEscapeChar(context).lower()

        news = News(context=context, parsed_context=parsed_context)
        return news


def removeEscapeChar(context): #Frontsize의 HTML 태그 제거
    import re
    str = re.sub("(<([^>]+)>)", "", context)
    str = str.replace('&nbsp;', "").replace('&lt;', "<").replace('&gt;', ">")\
        .replace('&amp;', "&").replace('&quot;', '"')
    return str
