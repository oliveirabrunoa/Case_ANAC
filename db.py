from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Voos(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ano = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    mercado = db.Column(db.String(300))
    rpk = db.Column(db.Integer)
