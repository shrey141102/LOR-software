# LoR Automation System 

## Endpoints Overview

- **`/`**: Homepage for uploading student documents.
  - **Method**: GET
  - **Description**: Renders a form to upload student documents including name, registration number, and PDF file.
  
- **`/uploads`**: Endpoint for handling document uploads.
  - **Method**: POST
  - **Description**: Accepts form data (student details and PDF file) and saves them to the database (`students.db`). Emails the uploaded document to selected faculty members.
  
- **`/documents`**: Endpoint to retrieve all uploaded documents.
  - **Method**: GET
  - **Description**: Returns a JSON list of all documents stored in the database (`students.db`).

- **`/delete_all_documents`**: Endpoint to delete all documents from the database.
  - **Method**: DELETE
  - **Description**: Deletes all documents stored in the database (`students.db`).

- **`/admin`**: Admin panel to view uploaded documents and manage the system.
  - **Method**: GET
  - **Description**: Renders an admin interface to view, search, and delete uploaded documents.

- **`/add_faculty`**: Endpoint to add new faculty members.
  - **Methods**: GET, POST
  - **Description**: GET renders a form to add a new faculty member. POST handles form submission to add the faculty member to the database.

- **`/list_faculty`**: Endpoint to list all existing faculty members.
  - **Method**: GET
  - **Description**: Renders a list of all faculty members stored in the database.

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

## File Structure

- `app.py`: Main Flask application file containing routes and database configurations.
- `templates/`: Directory containing HTML templates for rendering web pages.
- `static/`: Directory for storing static files such as CSS stylesheets and client-side scripts.
- `students.db`: SQLite database file storing uploaded document information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README now provides a concise overview of the endpoints available in your LoR Automation System project, along with setup instructions and other relevant details. Adjust as necessary based on your specific project requirements and additional features.