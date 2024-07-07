from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regno = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    faculty1 = db.Column(db.String(100), nullable=False)
    faculty2 = db.Column(db.String(100), nullable=True)
    faculty3 = db.Column(db.String(100), nullable=True)
    faculty1_ack = db.Column(db.Boolean, default=False)
    faculty2_ack = db.Column(db.Boolean, default=False)
    faculty3_ack = db.Column(db.Boolean, default=False)

    def get_faculty_details(self):
        faculty1 = Faculty.query.get(self.faculty1)
        faculty2 = Faculty.query.get(self.faculty2)
        faculty3 = Faculty.query.get(self.faculty3)
        return {
            'id': self.id,
            'regno': self.regno,
            'name': self.name,
            'filename': self.filename,
            'faculty1_name': faculty1.name if faculty1 else None,
            'faculty1_ack': self.faculty1_ack,
            'faculty2_name': faculty2.name if faculty2 else None,
            'faculty2_ack': self.faculty2_ack,
            'faculty3_name': faculty3.name if faculty3 else None,
            'faculty3_ack': self.faculty3_ack
        }



class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
