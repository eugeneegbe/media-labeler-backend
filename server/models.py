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


class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(255))
    filename = db.Column(db.String, unique=True, nullable=False)
    clarity = db.Column(db.Boolean)
    identity_type = db.Column(db.String)
    depict_accuracy = db.Column(db.String)
    subject_relevance = db.Column(db.String)
    accuracy = db.Column(db.String)
    created_at = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))
    region_alt = db.Column(db.String)
    region = db.Column(db.String)
    representation = db.Column(db.String)
    type = db.Column(db.String)

    def __repr__(self):
        # This is what is shown when object is printed
        return "User({}, {}, {})".format(
               self.id,
               self.username,
               self.type)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    filename = db.Column(db.String(255))
    category_id = db.Column(db.Integer)
    def __repr__(self):
        # This is what is shown when object is printed
        return "User({}, {})".format(
               self.id,
               self.username)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String)

    def __repr__(self):
        # This is what is shown when object is printed
        return "User({}, {})".format(
               self.id,
               self.name)

