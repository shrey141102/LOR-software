from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regno = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    faculty1 = db.Column(db.String(100), nullable=True)
    faculty2 = db.Column(db.String(100), nullable=True)
    faculty3 = db.Column(db.String(100), nullable=True)
    faculty1_ack = db.Column(db.Boolean, default=False)
    faculty2_ack = db.Column(db.Boolean, default=False)
    faculty3_ack = db.Column(db.Boolean, default=False)


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
