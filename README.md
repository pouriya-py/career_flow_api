# career_flow_api
# 🚀 CareerFlow API

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/Package%20Manager-uv-FF6B6B.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, intelligent, and scalable RESTful API for managing and matching job opportunities with user profiles. Designed with a focus on both local (IRAN) and global remote job markets.

## ✨ Features

- 🧠 **Smart Matching Algorithm:** Calculates skill match percentage between user profiles and job openings, highlighting missing skills.
- 🔍 **Advanced Filtering:** Filter jobs by market (Local/Global), remote status, source (e.g., LinkedIn, Jobinja), and text search.
- 🏗️ **Clean Architecture:** Modular structure using `APIRouter`, SQLAlchemy ORM, and Pydantic V2 for robust data validation.
- ⚡ **Blazing Fast:** Built with FastAPI and managed by the ultra-fast `uv` package manager.
- 🌱 **Seeded Database:** Comes with a ready-to-use seeding script for immediate testing and frontend development.

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite (Easily scalable to PostgreSQL via `.env`)
- **ORM:** SQLAlchemy
- **Validation:** Pydantic V2
- **Package Manager:** `uv` (Astral)

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager installed.

### Installation & Run

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/career_flow_api.git
   cd career_flow_api

2. Install dependencies using uv:
   ```bash
   uv sync

3. Seed the database with sample data (Jobs & a Test User):
   ```bash
   uv run python seed.py

4. Start the development server:
   ```bash
   uv run uvicorn app.main:app --reload

5. Open your browser and navigate to:
$ Interactive API Docs: http://127.0.0.1:8000/docs
$ Alternative Docs: http://127.0.0.1:8000/redoc

📂 Project Structure:
career_flow_api/
├── app/
│   ├── main.py           # Application entry point & CORS setup
│   ├── database.py       # SQLAlchemy engine & session management
│   ├── models.py         # Database models (ORM)
│   ├── schemas.py        # Pydantic models for validation
│   └── routes/           # API endpoints (users, jobs)
├── seed.py               # Script to populate database with mock data
├── pyproject.toml        # Project dependencies and metadata
└── README.md             # Project documentation

🔮 Roadmap (Next Steps)
$ Integration with n8n for automated job scraping and webhook ingestion.
$ Migration to PostgreSQL for production environment.
$ JWT Authentication for secure user endpoints.
$ Advanced pagination and sorting for job listings.
🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
📄 License
This project is licensed under the MIT License.