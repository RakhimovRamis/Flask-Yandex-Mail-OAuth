from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<login>:<password>@localhost/<db_name>?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['OAUTH'] = {"yandex":{"SERVICE": "yandex",
                                "CLIENT_ID": "<client_id>",
                                "CLIENT_SECRET": "<client_secret>",
                                "CALLBACK_URI": "http://localhost:5000/login/yandex/callback",
                                "URL": "https://oauth.yandex.ru/authorize",
                                "TOKEN_URL": "https://oauth.yandex.ru/token"},
                        "mail": {"SERVICE": "mail",
                                "CLIENT_ID": "<client_id>",
                                "CLIENT_SECRET": "<client_secret>",
                                "CALLBACK_URI": "http://localhost:5000/login/mail/callback",
                                "URL": "https://oauth.mail.ru/login",
                                "TOKEN_URL": "https://oauth.mail.ru/token"}}
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

import project.views
