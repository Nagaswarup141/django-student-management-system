# 📚 EduTrack — Student Management System

## 📁 Project Structure
```
FinalProject/
├── StudentMS/          ← Frontend (HTML single file)
│   ├── index.html      ← Open this in browser
│   └── README.md
│
└── Django_API/         ← Backend (Python Django + MySQL)
    ├── manage.py
    ├── requirements.txt
    ├── .env            ← DB password here
    ├── sms_project/    ← Django config
    ├── students/       ← Student CRUD API
    ├── courses/        ← Course API
    ├── attendance/     ← Attendance API
    ├── grades/         ← Grades API
    └── fees/           ← Fee API
```

---

## 🚀 Run (Windows)

### Step 1 — MySQL Database Create Cheyyi
```sql
CREATE DATABASE sms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 2 — VS Code lo Django_API Open Cheyyi
```
File → Open Folder → Django_API
```

### Step 3 — Terminal lo Run Cheyyi (oka okati)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4 — Environment Variables Set Cheyyi (every new terminal)
```bash
$env:DB_PASSWORD="Naga123@#"
$env:DB_NAME="sms_db"
$env:DB_USER="root"
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:SECRET_KEY="django-insecure-change-this-to-a-long-random-string"
```

### Step 5 — Migrations & Seed
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

### Step 6 — Server Start
```bash
python manage.py runserver
```
 


**Login:** `admin` / `admin123`
