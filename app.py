from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regno = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def upload():
    name = request.form['name']
    regno = request.form['regno']
    file = request.files['document']
    if file:
        filename = f"{regno}_{name}_{file.filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_document = Document(regno=regno, name=name, filename=filename)
        db.session.add(new_document)
        db.session.commit()
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


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
