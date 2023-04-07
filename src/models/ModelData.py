from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    __tablename__ = 'autos_toyota'

    id = db.Column(db.Integer, primary_key=True)
    link_href = db.Column(db.String(200))
    precio = db.Column(db.Float)
    modelo = db.Column(db.String(50))
    kilometraje = db.Column(db.Float)
    combustible = db.Column(db.String(40))



    