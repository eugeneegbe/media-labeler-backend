from datetime import datetime
from server.serializer import Serializer
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import LONGTEXT
from server import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        # This is what is shown when object is printed
        return "User({}, {})".format(
               self.id,
               self.username)


class Contribution(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(255))
    filename = db.Column(db.String(255), nullable=False)
    clarity = db.Column(db.String(30))
    identity_type = db.Column(db.String(30))
    depict_accuracy = db.Column(db.String(30))
    subject_relevance = db.Column(db.String(30))
    accuracy = db.Column(db.String(30))
    created_at = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))
    region_alt = db.Column(db.String(30))
    region = db.Column(db.String(30))
    representation = db.Column(db.String(30))
    type = db.Column(db.String(10))

    def serialize(self):
        return Serializer.serialize(self)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Contribution({}, {}, {})".format(
               self.id,
               self.username,
               self.type)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True)
    type = db.Column(db.String(10), nullable=False)

    def serialize(self):
        return Serializer.serialize(self)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Image({}, {})".format(
               self.id,
               self.name)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    filename = db.Column(db.String(255))
    url = db.Column(LONGTEXT)
    category_id = db.Column(db.Integer)
    description = db.Column(db.String(255))

    def serialize(self):
        return Serializer.serialize(self)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Image({}, {})".format(
               self.id,
               self.name)

