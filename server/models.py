from datetime import datetime

from flask_login import UserMixin

from server import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        # This is what is shown when object is printed
        return "User({}, {})".format(
               self.id,
               self.username)
