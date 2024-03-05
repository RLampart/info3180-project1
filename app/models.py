from . import db

class Property(db.Model):

    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(500))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    price = db.Column(db.Float)
    location = db.Column(db.String(80))
    type = db.Column(db.String(20))
    image = db.Column(db.String(80), unique = True)

    def __init__(self, title, description, bedrooms, bathrooms, price, location, type, image):
        self.title = title
        self.description = description
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.price = price
        self.location = location
        self.type = type
        self.image = image

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Property %r>' % (self.title)