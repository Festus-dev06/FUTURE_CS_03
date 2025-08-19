# 🔐 Secure File Sharing System  

## 📌 Project Overview
This project was developed as part of my **Cyber Security Internship (Future Interns – Task 3)**.  
The goal was to build a **Secure File Sharing System** where users can safely upload and download files.  
Security is the main focus — all files are **encrypted using AES** before storage and decrypted upon download.  

This simulates real-world client work in industries like **healthcare, finance, and corporate environments**, where data protection is critical.  

---

## ✨ Features
- ✅ Secure **file upload & download** functionality  
- ✅ **AES encryption** for files at rest  
- ✅ Basic **key management** for encryption/decryption  
- ✅ Simple **web interface** built with Flask & Jinja2  
- ✅ Safe handling of files in transit & storage  

---

## 🛠️ Tech Stack
- **Backend:** Python Flask  
- **Frontend:** HTML5, CSS3 (Jinja2 templates)  
- **Encryption:** AES (via PyCryptodome)  
- **Database:** SQLite (for file tracking)  
- **Version Control:** Git & GitHub  

---

## ⚙️ Installation & Setup
Follow the steps below to run the project locally:

```bash
# 1. Clone the repository
git clone https://github.com/Festus-dev06/FUTURE_CS_03.git
cd FUTURE_CS_03

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows
# source venv/bin/activate  # On Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask app
python app.py
