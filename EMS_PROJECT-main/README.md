# 🚨 Emergency Management System (EMS)

A Django-based **Emergency Management System (EMS)** that enables citizens to send SOS alerts with their live GPS location and allows emergency services to respond quickly through a centralized platform.

---

## 📌 Features

- 🔐 User Registration & Login
- 👤 Citizen Dashboard
- 🚑 One-click Emergency SOS
- 📍 Live GPS Location Sharing
- 🚓 Police Dashboard
- 🚒 Fire Department Dashboard
- 🏥 Hospital Dashboard
- 👨‍💼 Operator Dashboard
- 👥 Trusted Contact Notification
- 📋 Emergency History
- 🗂️ Admin Panel
- 📧 Email Notifications
- 📱 WhatsApp Notification Support (Twilio)

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Django
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite (Development)
- **Authentication:** Django Authentication
- **Email:** Gmail SMTP
- **Messaging:** Twilio WhatsApp API
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
EMS_PROJECT/
│── EMS/
│── users/
│── templates/
│── static/
│── manage.py
│── db.sqlite3
│── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/BhuvaPrashant085/EMS_PROJECT.git
```

### 2. Move to the Project Folder

```bash
cd EMS_PROJECT
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## 🔧 Environment Variables

Store sensitive credentials as environment variables instead of hardcoding them.

Example:

```
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

---

## 📸 Screenshots

Add screenshots here.

- Login Page
- Citizen Dashboard
- Emergency Alert
- Police Dashboard
- Hospital Dashboard
- Fire Dashboard

---

## 🚀 Future Improvements

- REST API using Django REST Framework
- JWT Authentication
- Real-time Emergency Tracking
- Google Maps Integration
- Push Notifications
- SMS Alerts
- Android Application

---

## 👨‍💻 Author

**Prashant Bhuva**

- GitHub: https://github.com/BhuvaPrashant085
- LinkedIn: https://www.linkedin.com/in/prashant-bhuva/
- Website : https://prashantbhuva.vercel.app/




---

## 📄 License

This project is intended for educational and portfolio purposes.


