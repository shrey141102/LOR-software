import sqlalchemy.exc
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Document, Faculty
from flask_mail import Mail, Message
import os
import uuid
from instance.config import Config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
# app.config.from_object('config.Config')
# app.config.from_pyfile('config.py')

db.init_app(app)
mail = Mail(app)

with app.app_context():
    db.create_all()

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
        new_document = Document(
            regno=regno,
            name=name,
            filename=filename,
            faculty1=faculty_ids[0] if faculty_ids[0] else None,
            faculty2=faculty_ids[1] if len(faculty_ids) > 1 and faculty_ids[1] else None,
            faculty3=faculty_ids[2] if len(faculty_ids) > 2 and faculty_ids[2] else None
        )
        faculties = Faculty.query.filter(Faculty.id.in_(faculty_ids)).all()

        db.session.add(new_document)
        db.session.commit()

        send_email(regno, faculties, filepath, new_document)

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


@app.route('/admin', methods=['GET'])
def admin_panel():
    documents = Document.query.all()
    documents_with_faculty = [doc.get_faculty_details() for doc in documents]
    return render_template('admin.html', documents=documents_with_faculty)


from flask import flash

@app.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        school = request.form['school']
        new_faculty = Faculty(id=id, name=name, email=email, school=school)
        try:
            db.session.add(new_faculty)
            db.session.commit()
            return redirect(url_for('list_faculty'))
        except Exception as e:
            db.session.rollback()
            flash("Error: Faculty ID already exists. Please enter a unique ID.")
            return redirect(url_for('add_faculty'))
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

@app.route('/acknowledge_receipt/<string:student_id>/<int:faculty_id>/<int:document_id>', methods=['GET'])
def acknowledge_receipt(student_id, document_id, faculty_id):
    faculty_id = (str)(faculty_id)
    document = Document.query.filter_by(id=document_id).first_or_404()
    if document.regno != student_id:
        return jsonify({'error': 'Registration number does not match'}), 400
    print(type(document.faculty1))
    if faculty_id == document.faculty1:
        document.faculty1_ack = True
    elif faculty_id == document.faculty2:
        document.faculty2_ack = True
    elif faculty_id == document.faculty3:
        document.faculty3_ack = True
    else:
        return jsonify({'error': 'Invalid faculty_id'}), 400  # Return an error if faculty_id is not recognized

    db.session.commit()

    # return jsonify({'success': True})
    return render_template('approval_page.html')


def send_email(regno, faculties, filepath, document):
    for idx, faculty in enumerate(faculties):
        with app.open_resource(filepath) as fp:
            confirmation_link = url_for('acknowledge_receipt', student_id=regno, faculty_id=faculty.id, document_id=document.id, _external=True)
            msg = Message(
                subject="TEST EMAIL FOR LOR SOFTWARE",
                recipients=[faculty.email],
                body=f"Dear {faculty.name},\n\nA new document has been uploaded.\n\nBest regards,\nYour Team"
            )
            msg.attach(filename=filepath, content_type="application/pdf", data=fp.read())
            msg.html = render_template('email_template.html', faculty_name=faculty.name, student_name=document.name, regno=document.regno, confirmation_link=confirmation_link)
            mail.send(msg)



if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
