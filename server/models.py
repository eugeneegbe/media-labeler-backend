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
    filename = db.Column(db.String(255), unique=True, nullable=False)
    clarity = db.Column(db.Boolean)
    identity_type = db.Column(db.String(30))
    depict_accuracy = db.Column(db.String(30))
    subject_relevance = db.Column(db.String(30))
    accuracy = db.Column(db.String(30))
    created_at = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))
    region_alt = db.Column(db.String(30))
    region = db.Column(db.String(30))
    representation = db.Column(db.String(30))
    type = db.Column(db.String(10))

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
    file_name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __repr__(self):
        # This is what is shown when object is printed
        return "User({}, {})".format(
               self.id,
               self.name)

