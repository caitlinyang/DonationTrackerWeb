from donationTracker import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username, self.email, self.user_type)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.String(20), nullable=False)
    long = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(11), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    website = db.Column(db.String(100), nullable=False)
    items = db.relationship('Item', backref='location', lazy=True)

    def __repr__(self):
        return "Location('{}', '{}', '{}')".format(self.name, self.city, self.type)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
