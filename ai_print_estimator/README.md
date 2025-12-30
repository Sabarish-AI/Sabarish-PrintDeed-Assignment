# 🖨️ AI Print Estimator

An intelligent, containerized application that automatically estimates printing costs using configurable business rules and AI-assisted logic. Built to solve real-world pricing challenges in print businesses by eliminating manual calculations, reducing errors, and accelerating quotation workflows.

---

## 🚀 Project Overview

**AI Print Estimator** is a production-ready system that calculates accurate print job costs based on parameters such as dimensions, material type, quantity, and finishing options.

This project demonstrates:
- Strong Python backend development
- Practical AI-assisted decision logic
- Clean REST API design
- Docker & DevOps fundamentals
- Real-world business problem solving

---

## ✨ Key Features

- 📐 Dynamic cost estimation based on print specifications  
- 🤖 AI-assisted pricing logic for optimized estimates  
- ⚙️ Configurable pricing engine (business-rule driven)  
- 🐳 Fully Dockerized setup using Docker Compose  
- 🌐 Simple web-based user interface  
- 🔄 Scalable and extensible architecture  

---

## 🛠️ Tech Stack

- **Backend:** Python  
- **API Framework:** FastAPI / Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Containerization:** Docker, Docker Compose  
- **Deployment:** Localhost (Cloud-ready)

---

## 📂 Project Structure
ai_print_estimator/
├── backend/
│ ├── main.py
│ ├── estimator/
│ │ ├── pricing_engine.py
│ │ └── ai_logic.py
│ └── requirements.txt
├── frontend/
│ ├── index.html
│ ├── styles.css
│ └── script.js
├── Dockerfile
├── docker-compose.yml
└── README.md

## ▶️ How to Run the Project

### Prerequisites
- Docker
- Docker Compose

### Build & Run
```bash
docker compose up --build

Access the Application

UI: http://localhost:8000

API Docs: http://localhost:8000/docs

(Port may vary based on configuration)

🧠 How It Works

User enters print job details via the UI

Backend validates the input

AI-assisted pricing engine processes the request

Estimated cost is returned instantly

📈 Real-World Use Cases

Print and flex banner businesses

Automated quotation systems

Online print ordering platforms

Internal pricing tools for sales teams

🔮 Future Enhancements

Machine learning–based dynamic pricing

Historical pricing analytics dashboard

Database integration

Authentication and role-based access

Cloud deployment (AWS / GCP / Azure)

👨‍💻 Author

Sabarish Subramanian
Python Developer | AI & Automation Enthusiast
