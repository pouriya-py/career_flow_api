# 🚀 CareerFlow - AI-Powered Job Matching Platform

https://career-flow-api.onrender.com

<div align="center">

![CareerFlow](https://img.shields.io/badge/CareerFlow-AI%20Powered-8b5cf6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNMjAgNyhsLTgtNC04IDRtMTYgMGwtOCA0bS04LTR2MTBsOCA0bTAtMTBsOCA0Ij48L3BhdGg+PC9zdmc+)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An intelligent job matching system that automatically scrapes opportunities from 5+ international sources, matches them to user profiles using AI algorithms, and delivers personalized recommendations via Telegram and email.**

[🌟 Features](#-features) • [🛠️ Tech Stack](#️-tech-stack) • [📦 Installation](#-installation) • [🐳 Docker](#-docker-deployment) • [🧪 Testing](#-testing) • [📡 API](#-api-documentation)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#️-tech-stack)
- [Installation](#-installation)
- [Docker Deployment](#-docker-deployment)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Security](#-security)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

CareerFlow is a production-ready, full-stack job matching platform that solves the problem of finding relevant job opportunities in a crowded market. It combines:

- **Automated Data Collection**: Scrapes jobs from 5+ international sources every 30 minutes
- **Intelligent Matching**: Uses a multi-factor scoring algorithm to match jobs to user profiles
- **Real-time Notifications**: Delivers personalized recommendations via Telegram bot and email
- **Modern UI**: Beautiful, responsive dark-themed dashboard with real-time analytics
- **Enterprise-Grade Infrastructure**: Docker, PostgreSQL, automated testing, and professional logging

---

## ✨ Features

### 🤖 Automation & Intelligence
- **Multi-Source Job Scraping**: Automatically fetches jobs from:
  - Remotive API (Remote Python jobs)
  - WeWorkRemotely (RSS feed)
  - RemoteOK (RSS feed)
  - Python.org Jobs (RSS feed)
  - Hacker News "Who is Hiring" (RSS feed)

- **Smart Matching Algorithm**: Scores jobs based on:
  - Skill compatibility (70% weight)
  - Target market alignment (15% weight)
  - Remote work preference (10% weight)
  - Experience level (5% weight)

- **Scheduled Tasks**: 
  - Job scraper runs every 30 minutes
  - Daily job delivery to Telegram users at 9 AM
  - Configurable via APScheduler

### 📱 User Experience
- **Modern Frontend**: Dark theme with purple gradient, animations, and Chart.js visualizations
- **Telegram Bot**: 
  - User verification via activation codes
  - On-demand job recommendations (`/matches` command)
  - Automated daily job delivery
- **Email Notifications**: Welcome emails with activation codes (SMTP support)
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

### 🔐 Security & Performance
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt with automatic salt generation
- **Rate Limiting**: 60 requests per minute per IP
- **IP Blocking**: Admin can block malicious IPs
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic schemas for all API endpoints

### 📊 Admin Panel
- **SQLAdmin Integration**: Professional admin interface
- **User Management**: View, edit, and manage users
- **Job Source Control**: Enable/disable job sources
- **Job Moderation**: Review and manage job opportunities
- **IP Blocking**: Block/unblock IPs from admin panel
- **Statistics API**: JSON endpoint for system metrics (`/api/stats`)

### 🛠️ Developer Experience
- **Type Safety**: Full type hints with Pydantic and SQLAlchemy
- **Auto-generated Docs**: Swagger UI and ReDoc
- **Professional Logging**: Loguru with file rotation
- **Automated Testing**: pytest with 5 comprehensive tests
- **Docker Support**: One-command deployment
- **Hot Reload**: Fast development with `--reload` flag

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │  HTML5 + Tailwind CSS + Chart.js
│   (Browser)     │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI       │  Python 3.12+
│   Backend       │  JWT Auth, Rate Limiting
└────────┬────────┘
         │
    ┌────┴────┬────────────┬─────────────┐
    ▼         ▼            ▼             ▼
┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│PostgreSQL│ │Telegram  │ │Email     │ │Background│
│Database │ │Bot       │ │Service   │ │Tasks     │
│        │ │(Aiogram) │ │(SMTP)    │ │(APSch.)  │
└────────┘ └──────────┘ └──────────┘ └──────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern, fast web framework |
| **SQLAlchemy 2.0** | ORM for database management |
| **PostgreSQL 15** | Production-ready database |
| **Pydantic V2** | Data validation and settings |
| **APScheduler** | Background task scheduling |
| **Aiogram 3.x** | Telegram bot framework |
| **aiosmtplib** | Async email sending |
| **python-jose** | JWT token handling |
| **passlib + bcrypt** | Password hashing |
| **slowapi** | Rate limiting |
| **Loguru** | Professional logging |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5** | Semantic markup |
| **Tailwind CSS** | Utility-first CSS framework |
| **Chart.js** | Interactive charts and graphs |
| **Vanilla JavaScript** | No framework overhead |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |
| **PostgreSQL** | Relational database |
| **Mailpit** | Email testing (development) |
| **uv** | Fast Python package manager |

### Testing & Quality
| Technology | Purpose |
|------------|---------|
| **pytest** | Automated testing framework |
| **httpx** | Async HTTP client for tests |
| **pytest-asyncio** | Async test support |

---

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)
- Git
- PostgreSQL 15+ (optional, SQLite works for development)

### Step 1: Clone the Repository
```bash
git clone https://github.com/pouriya-py/career_flow_api.git
cd career_flow_api
```

### Step 2: Install Dependencies
```bash
uv sync
```

### Step 3: Configure Environment Variables
Create a `.env` file in the root directory:
```env
# Telegram Bot Token (get from @BotFather)
BOT_TOKEN=your_telegram_bot_token_here

# Database (SQLite for development, PostgreSQL for production)
DATABASE_URL=sqlite:///./career_flow.db
# DATABASE_URL=postgresql://user:password@localhost:5432/careerflow

# Email Configuration (Mailpit for local testing)
SMTP_HOST=localhost
SMTP_PORT=1025
FROM_EMAIL=noreply@careerflow.local

# JWT Secret Key (CHANGE THIS IN PRODUCTION!)
SECRET_KEY=your-super-secret-key-change-in-production
```

### Step 4: Initialize Database
```bash
# Create tables and seed initial data
uv run python seed.py

# Fetch initial jobs from all sources
uv run python test_scraper.py
```

### Step 5: Start the Server
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at:
- **Frontend**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **Admin Panel**: http://127.0.0.1:8000/admin (credentials: `admin` / `admin123`)
- **Statistics API**: http://127.0.0.1:8000/api/stats

---

## 🐳 Docker Deployment

The easiest way to run CareerFlow in production is with Docker Compose.

### Prerequisites
- Docker Desktop (Mac/Windows) or Docker Engine (Linux)
- Docker Compose v2+

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/pouriya-py/career_flow_api.git
cd career_flow_api

# 2. Create .env file
cp .env.example .env
# Edit .env and add your BOT_TOKEN

# 3. Start all services
docker-compose up --build -d

# 4. Initialize database
docker exec -it careerflow_app uv run python seed.py
docker exec -it careerflow_app uv run python test_scraper.py
```

### Access Points
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:8000/admin
- **Mailpit UI**: http://localhost:8025 (email testing)
- **PostgreSQL**: localhost:5432

### Docker Commands
```bash
# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build -d

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up --build -d
```

---

## 📖 Usage Guide

### 1. Register a User
1. Visit http://127.0.0.1:8000
2. Click "Login / Register"
3. Fill in the registration form:
   - Username
   - Password (min 6 characters)
   - Email
   - Experience years
   - Target market (Global/Iran)
   - Skills (comma-separated, e.g., "Python, FastAPI, Docker")
   - Favorite job sources

4. After registration, you'll receive an **activation code** (e.g., `ACT-A1B2C3D4`)

### 2. Connect Telegram Bot
1. Open Telegram and search for your bot (created via @BotFather)
2. Send `/start` command
3. Send your activation code (e.g., `ACT-A1B2C3D4`)
4. Your account is now connected!

### 3. Get Job Recommendations
- **On-demand**: Send `/matches` command to the bot
- **Automatic**: Receive daily job recommendations at 9 AM

### 4. View Dashboard
The dashboard shows:
- Total jobs in database
- Remote jobs count
- Active job sources
- Your match score
- Charts: Job distribution by source, Top skills in demand

### 5. Admin Panel
1. Visit http://127.0.0.1:8000/admin
2. Login with `admin` / `admin123`
3. Manage users, job sources, jobs, and blocked IPs
4. View system statistics at http://127.0.0.1:8000/api/stats

---

## 📡 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Key Endpoints

#### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create new user |
| POST | `/users/login` | Login and get JWT token |
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update user profile |

#### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/jobs/` | Get all jobs (limit: 100) |
| GET | `/jobs/matches` | Get personalized job matches (requires auth) |
| POST | `/jobs/webhook/jobs` | Receive jobs from external webhook |

#### Sources
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sources/` | Get all job sources |
| GET | `/sources/active` | Get active job sources |

#### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/stats` | System statistics (JSON) |

---

## 🧪 Testing

CareerFlow includes comprehensive automated tests to ensure reliability.

### Run All Tests
```bash
uv run pytest -v
```

### Test Coverage
- ✅ Health check endpoint
- ✅ User registration (success and duplicate prevention)
- ✅ Job matching algorithm (perfect and partial matches)
- ✅ Authentication flow
- ✅ API response validation

### Example Test Output
```
tests/test_api.py::test_health_check PASSED
tests/test_api.py::test_user_registration_success PASSED
tests/test_api.py::test_user_registration_duplicate PASSED
tests/test_matching.py::test_matching_algorithm_perfect_match PASSED
tests/test_matching.py::test_matching_algorithm_partial_match PASSED

============================================ 5 passed in 1.23s =============================================
```

---

## 📁 Project Structure

```
career_flow_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # SQLAlchemy database models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── auth.py                 # JWT authentication logic
│   ├── middleware.py           # IP blocking middleware
│   ├── database.py             # Database configuration
│   ├── tasks.py                # Background tasks (scraper, bot)
│   ├── core/
│   │   └── logger.py           # Loguru configuration
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py            # User endpoints
│   │   ├── jobs.py             # Job endpoints
│   │   └── sources.py          # Source endpoints
│   └── services/
│       ├── email_service.py    # Email sending logic
│       └── matching_service.py # Job matching algorithm
├── static/
│   └── index.html              # Frontend application
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── test_api.py             # API endpoint tests
│   └── test_matching.py        # Matching algorithm tests
├── .env                        # Environment variables (not in git)
├── .gitignore
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Multi-container setup
├── pytest.ini                  # Pytest configuration
├── pyproject.toml              # Python dependencies
├── uv.lock                     # Locked dependencies
├── seed.py                     # Database seeder
├── test_scraper.py             # Manual scraper test
└── README.md                   # This file
```

---

## 🔒 Security

### Best Practices Implemented
- ✅ Password hashing with bcrypt (automatic salt)
- ✅ JWT token authentication
- ✅ Rate limiting (60 requests/minute)
- ✅ IP blocking system
- ✅ CORS protection
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS protection (FastAPI default)

### Production Checklist
Before deploying to production:
1. **Change SECRET_KEY** in `.env` to a strong random string
2. **Change admin password** in `app/main.py` (AdminAuth class)
3. **Use PostgreSQL** instead of SQLite
4. **Enable HTTPS** with SSL certificates
5. **Set up proper email provider** (SendGrid, AWS SES, etc.)
6. **Configure firewall** and restrict access
7. **Enable database backups**
8. **Set up monitoring** and alerting

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use type hints
- Keep functions small and focused

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Job data sourced from: Remotive, WeWorkRemotely, RemoteOK, Python.org, Hacker News
- Built with [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/), and [Aiogram](https://docs.aiogram.dev/)
- UI inspired by modern dark theme designs
- Icons from [Font Awesome](https://fontawesome.com/)

---

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on [GitHub](https://github.com/pouriya-py/career_flow_api/issues)
- Contact the author: [@pouriya-py](https://github.com/pouriya-py)

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star on GitHub! ⭐**

**Made with ❤️ by [Pouriya](https://github.com/pouriya-py)**

</div>
```
