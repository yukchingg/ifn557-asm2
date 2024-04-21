from . import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'defaultteam.jpg')
    jerseys = db.relationship('Jersey', backref='Team', cascade="all, delete-orphan")

    def __repr__(self):
        str = "ID: {}, Name: {}, Description: {}, Image: {}\n" 
        str = str.format(self.id, self.name, self.description, self.image)
        return str

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('jersey_id',db.Integer,db.ForeignKey('jerseys.id'), nullable=False),
    db.PrimaryKeyConstraint('order_id', 'jersey_id') )

class Jersey(db.Model):
    __tablename__ = 'jerseys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    number = db.Column(db.Integer, nullable= False)
    price = db.Column(db.Float, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    
    def __repr__(self):
        str = "ID: {}, Name: {}, Description: {}, Image: {}, Number:{}, Price: {}, Team: {}\n" 
        str = str.format(self.id, self.name, self.description, self.image, self.number, self.price, self.team_id)
        return str

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    address = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    jerseys = db.relationship("Jersey", secondary=orderdetails, backref="jerseys")
    
    def __repr__(self):
        str = "ID: {}, Status: {}, First Name: {}, Surname:{}, Address: {}, Email: {}, Phone: {}, Date: {}, Jerseys: {}, Total Cost: {}\n" 
        str = str.format(self.id, self.status, self.firstname, self.surname, self.address, self.email, self.phone, self.date, self.jerseys, self.totalcost)
        return str
