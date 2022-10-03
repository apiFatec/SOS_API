from app import db

class Address(db.Model):
  id = db.Column(db.Interger, primary_key=True, nullable=False)
  lab = db.Column(db.String, nullable=False)
  num = db.Column(db.String, nullable=False)
  patrimony = db.Column(db.String)
  computer = db.relationship("Computers", backref="address", lazy=True)