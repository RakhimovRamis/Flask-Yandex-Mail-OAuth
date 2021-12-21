from project import db, UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True, nullable=False)

    def __repr__(self):
        return f'User {self.id}'