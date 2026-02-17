# Talent Flow - Full Stack Employee Management System

A clean, modular, and professional Human Resource Management System. This project demonstrates a full-stack application with a **Flask** backend, **SQLAlchemy** ORM, and a responsive **Bootstrap 5** frontend.

## 🚀 Features

- **Employee Management**: Create, view, update, and delete employee records.
- **Attendance Tracking**: Real-time check-in/check-out and attendance history.
- **Reporting**: Visual analytics of employee distribution by department.
- **REST API**: Comprehensive JSON endpoints for all operations.

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js, Jinja2 Templates
- **Backend**: Python 3.8+, Flask 3.x
- **Database**: SQLite (Development), SQLAlchemy ORM

## 📂 Project Structure

```bash
hrms-project/
├── app/
│   ├── models/          # Database Models
│   ├── routes/          # API & Web Routes
│   ├── services/        # Business Logic
│   ├── templates/       # HTML Templates
│   └── static/          # CSS, JS, Images
├── instance/            # SQLite Database
├── config.py            # App Configuration
└── run.py               # Entry Point
```

## ⚡ Setup & Run

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd hrms-project
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Application**:
    ```bash
    python run.py
    ```
    Access the app at `http://localhost:5001`. The database will be created automatically.

## 📖 API Documentation

Full API documentation is available at `http://localhost:5001/api` when the server is running.