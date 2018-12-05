from datetime import datetime
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
    name = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    def __repr__(self):
        return "Item('{}', '{}', '{}')".format(self.name, self.category, self.location_id)

location_1 = Location(name="AFD Station", lat="33.75416", long="-84.37742", address="309 EDGEWOOD AVE SE",city="Atlanta",state="GA",zip="30332",type="Drop Off",phone="(404) 555 - 3456",website="www.afd04.atl.ga")
location_2 = Location(name="BOYS & GIRLS CLUB W.W. WOOLFOLK", lat="33.73182", long="-84.43871", address="1642 RICHLAND RD",city="Atlanta",state="GA",zip="30332",type="Store",phone="(404) 555 - 1234",website="www.bgc.wool.ga")
location_3 = Location(name="PATHWAY UPPER ROOM CHRISTIAN MINISTRIES", lat="33.70866", long="-84.41853", address="1683 SYLVAN RD",city="Atlanta",state="GA",zip="30332",type="Warehouse",phone="(404) 555 - 5432",website="www.pathways.org")
location_4 = Location(name="PAVILION OF HOPE INC", lat="33.80129", long="-84.25537", address="3558 EAST PONCE DE LEON AVE",city="SCOTTDALE",state="GA",zip="30079",type="Warehouse",phone="(404) 555 - 8765",website="www.pavhope.org")
location_5 = Location(name="D&D CONVENIENCE STORE", lat="33.71747", long="-84.2521", address="2426 COLUMBIA DRIVE",city="DECATUR",state="GA",zip="30034",type="Drop Off",phone="(404) 555 - 9876",website="www.ddconv.com")
location_6 = Location(name="KEEP NORTH FULTON BEAUTIFUL", lat="33.96921", long="-84.3688", address="470 MORGAN FALLS RD",city="Sandy Springs",state="GA",zip="30302",type="Store",phone="(770) 555 - 7321",website="www.knfb.org")
