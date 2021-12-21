from flask import redirect, url_for, request
from project import app, login_manager, db
from project.models import User
from flask_login import login_required, current_user, logout_user, login_user
import requests

class OAuth:
    def __init__(self, oauth_service):
        self.oauth_service = app.config['OAUTH'].get(oauth_service, None)

    @property
    def config(self):
        return self.oauth_service

    @property
    def redirect_uri(self):
        uri = f"{self.oauth_service['URL']}?response_type=code"\
                f"&client_id={self.oauth_service['CLIENT_ID']}"\
                f"&redirect_uri={self.oauth_service['CALLBACK_URI']}"\
                "&state=0"
        print(uri)
        return uri
        
    def get_token(self, code):
        data = {"grant_type": "authorization_code",
                "code": code,
                "client_id": self.oauth_service['CLIENT_ID'],
                "client_secret": self.oauth_service['CLIENT_SECRET'],
                "redirect_uri": self.oauth_service['CALLBACK_URI']}
        return requests.post(self.oauth_service["TOKEN_URL"], data=data).json()

    def user_info_yandex(self, code):
        headers = {"Authorization": f"OAuth {self.get_token(code)['access_token']}"}
        res = requests.get('https://login.yandex.ru/info?format=json', headers=headers).json()
        info = {'id': f"ya_{res.get('id')}",
                'email': res.get('default_email', None),
                'username': res.get('real_name', None)}
        return info

    def user_info_mail(self, code):
        res =  requests.get(f'https://oauth.mail.ru/userinfo?access_token={self.get_token(code)["access_token"]}').json()
        info = {'id': f"ma_{res.get('id')}",
                'email': res.get('email', None),
                'username': res.get('name', None)}
        return info

    def user_info(self, code):
        result = getattr(self, f'user_info_{self.oauth_service["SERVICE"]}')(code)
        return result

@login_manager.user_loader
def load_user(id_user):
    user = User.query.filter_by(id=id_user).first()
    return user

@app.route('/login/<oauth_service>')
def login_oauth(oauth_service):
    oauth = OAuth(oauth_service)
    if oauth.config:
        return redirect(oauth.redirect_uri)
    return redirect(url_for('index'))

@app.route('/login/<oauth_service>/callback')
def callback(oauth_service):
    oauth = OAuth(oauth_service)
    if oauth.config:
        user_info = oauth.user_info(request.args.get('code', None))
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(login=user_info['id'],
                        email=user_info['email'],
                        username=user_info['username'])
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('manager'))
    return redirect(url_for('index'))

@app.route('/manager')
@login_required
def manager():
    return f''' <b>User: </b>{current_user.username}<br>
                <b>Email: </b>{current_user.email}
            '''

@app.route('/')
@app.route('/login')
def index():
    return f'''<b>Войти</b><br>
                <a href="/login/yandex">Yandex</a>
                <a href="/login/mail">Mail</a>
            '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
