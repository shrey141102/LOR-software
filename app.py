from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Document, Faculty
from flask_mail import Mail, Message
import os
from instance.config import Config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
# app.config.from_object('config.Config')
# app.config.from_pyfile('config.py')

db.init_app(app)

mail = Mail(app)

@app.route('/')
def index():
    faculties = Faculty.query.all()
    return render_template('index.html', faculties=faculties)

@app.route('/uploads', methods=['POST'])
def upload():
    name = request.form['name']
    regno = request.form['regno']
    file = request.files['document']
    faculty_ids = []
    for i in range(1, 4):
        faculty_id = request.form.get(f'faculty{i}')
        if faculty_id:
            faculty_ids.append(faculty_id)
    if file:
        filename = f"{regno}_{name}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        new_document = Document(regno=regno, name=name, filename=filename)
        db.session.add(new_document)
        db.session.commit()

        faculties = Faculty.query.filter(Faculty.id.in_(faculty_ids)).all()
        send_email(faculties, filepath)

        return redirect(url_for('index'))

@app.route('/documents', methods=['GET'])
def get_documents():
    documents = Document.query.all()
    result = []
    for document in documents:
        result.append({
            'id': document.id,
            'regno': document.regno,
            'name': document.name,
            'filename': document.filename
        })
    return jsonify(result)

@app.route('/delete_all_documents', methods=['GET'])
def delete_all_documents():
    try:
        db.session.query(Document).delete()
        db.session.commit()
        return jsonify({'message': 'All documents deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

@app.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_faculty = Faculty(name=name, email=email)
        db.session.add(new_faculty)
        db.session.commit()
        return redirect(url_for('list_faculty'))
    return render_template('add_faculty.html')

@app.route('/delete_all_faculty', methods=['GET'])
def delete_all_faculty():
    try:
        db.session.query(Faculty).delete()
        db.session.commit()
        return jsonify({'message': 'All faculty deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/list_faculty', methods=['GET'])
def list_faculty():
    faculties = Faculty.query.all()
    return render_template('list_faculty.html', faculties=faculties)

def send_email(faculties, filepath):
    with app.open_resource(filepath) as fp:
        for faculty in faculties:
            msg = Message(
                subject="New Document Uploaded",
                recipients=[faculty.email]
            )
            msg.body = f"Dear {faculty.name},\n\nA new document has been uploaded.\n\nBest regards,\nYour Team"
            msg.attach(filename=filepath, content_type="application/pdf", data=fp.read())
            mail.send(msg)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
