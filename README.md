# LoR Automation System (In progress)

## Features

- **Document Upload**: Users can upload PDF documents along with student details such as name and registration number.
- **Database Storage**: Documents are stored in a SQLite database (`students.db`) with attributes including document ID, registration number, student name, and filename.
- **Admin Panel**: An admin interface (`/admin`) allows administrators to view all uploaded documents, including options for deletion.
- **Responsive Design**: The web interface is designed to be user-friendly and responsive across different devices.

## Technologies Used

- **Flask**: Python web framework used for backend development.
- **SQLAlchemy**: Object-relational mapping (ORM) library for Python, used with Flask to interact with the SQLite database.
- **HTML/CSS**: Frontend components for user interaction and admin panel layout.
- **JavaScript (AJAX)**: Used for asynchronous data fetching to dynamically update the admin panel.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Setup Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**:
   ```bash
   python app.py
   ```

5. **Run the Application**:
   ```bash
   flask run
   ```

6. **Access the Application**:
   Open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage

- **Uploading Documents**: Navigate to the homepage (`/`) to upload documents. Enter student details (name, registration number) and select a PDF file to upload.
- **Admin Panel**: Visit the admin panel (`/admin`) to view all uploaded documents. Administrators can delete documents from this interface.

## File Structure

- `app.py`: Main Flask application file containing routes and database configurations.
- `templates/`: Directory containing HTML templates for rendering web pages.
- `static/`: Directory for storing static files such as CSS stylesheets and client-side scripts.
- `students.db`: SQLite database file storing uploaded document information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
