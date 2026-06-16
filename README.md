
```markdown
# 🚀 CareerFlow - AI-Powered Job Matching Platform

<div align="center">

![CareerFlow Logo](https://img.shields.io/badge/CareerFlow-AI%20Powered-8b5cf6?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Smart job matching system that scrapes job sites, matches jobs to user profiles based on skills and preferences, and notifies users via Telegram and email.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation)

</div>

---

## ✨ Features

### 🎯 Core Features
- **Multi-Source Job Scraping**: Automatically fetches jobs from 5+ international sources every 30 minutes
  - Remotive API
  - WeWorkRemotely (RSS)
  - RemoteOK (RSS)
  - Python.org Jobs (RSS)
  - Hacker News Who is Hiring (RSS)

- **AI-Powered Job Matching**: Smart algorithm that scores jobs based on:
  - Skill compatibility (70% weight)
  - Target market alignment (15% weight)
  - Remote work preference (10% weight)
  - Experience level (5% weight)

- **Telegram Bot Integration**: 
  - User verification via activation codes
  - On-demand job recommendations (`/matches` command)
  - Daily automated job delivery at 9 AM

- **Email Notifications**: Welcome emails with activation codes (SMTP support)

- **Modern Frontend**: 
  - Dark theme with purple gradient design
  - Real-time charts and statistics
  - Responsive design (mobile-friendly)
  - Hash-based routing

### 🔐 Security & Performance
- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting (60 requests/minute)
- IP blocking system
- CORS protection

### 📊 Admin Panel
- SQLAdmin integration for managing:
  - Users
  - Job sources
  - Job opportunities
  - Blocked IPs

---

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database management
- **SQLite** - Lightweight database (easily switchable to PostgreSQL)
- **Pydantic** - Data validation
- **APScheduler** - Background task scheduling
- **Aiogram** - Telegram bot framework
- **aiosmtplib** - Async email sending

### Frontend
- **HTML5 + Tailwind CSS** - Modern UI framework
- **Chart.js** - Interactive charts
- **Vanilla JavaScript** - No framework overhead

### Tools & Libraries
- **httpx** - Async HTTP client
- **feedparser** - RSS feed parsing
- **python-jose** - JWT token handling
- **passlib** - Password hashing
- **slowapi** - Rate limiting

---

## 📦 Installation

### Prerequisites
- Python 3.12+
- uv (Python package manager)
- Git

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
BOT_TOKEN=your_bot_token_here

# Email Configuration (for local testing with Mailpit)
SMTP_HOST=localhost
SMTP_PORT=1025
FROM_EMAIL=noreply@careerflow.local

# JWT Secret Key (change this in production!)
SECRET_KEY=your-secret-key-change-in-production
```

### Step 4: Initialize Database
```bash
# Create database tables and seed initial data
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
- **Admin Panel**: http://127.0.0.1:8000/admin (username: `admin`, password: `admin123`)

---

## 🚀 Usage

### 1. Register a User
Visit http://127.0.0.1:8000 and click "ورود / ثبت‌نام" (Login / Register)

Fill in the registration form:
- Username
- Password (min 6 characters)
- Email
- Experience years
- Target market (Global/Iran)
- Skills (comma-separated)
- Favorite job sources

After registration, you'll receive an **activation code** (e.g., `ACT-A1B2C3D4`)

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

---

## 📡 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Key Endpoints

#### Users
- `POST /users/` - Create new user
- `POST /users/login` - Login and get JWT token
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile

#### Jobs
- `GET /jobs/` - Get all jobs (limit: 100)
- `GET /jobs/matches` - Get personalized job matches (requires authentication)
- `POST /jobs/webhook/jobs` - Receive jobs from external webhook

#### Sources
- `GET /sources/` - Get all job sources
- `GET /sources/active` - Get active job sources

---

## 📁 Project Structure

```
career_flow_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── auth.py                 # JWT authentication
│   ├── middleware.py           # IP blocking middleware
│   ├── database.py             # Database configuration
│   ├── tasks.py                # Background tasks (scraper, bot)
│   ├── routes/
│   │   ├── users.py            # User endpoints
│   │   ├── jobs.py             # Job endpoints
│   │   └── sources.py          # Source endpoints
│   └── services/
│       ├── email_service.py    # Email sending logic
│       └── matching_service.py # Job matching algorithm
├── static/
│   └── index.html              # Frontend application
├── .env                        # Environment variables (not in git)
├── .gitignore
├── pyproject.toml              # Python dependencies
├── uv.lock                     # Locked dependencies
├── seed.py                     # Database seeder
├── test_scraper.py             # Manual scraper test
└── README.md                   # This file
```

---

## 🔄 Background Tasks

The system runs two automated tasks:

1. **Job Scraper** (every 30 minutes):
   - Fetches jobs from 5 sources
   - Saves new jobs to database
   - Prevents duplicates

2. **Daily Job Delivery** (9 AM daily):
   - Sends personalized job recommendations to all verified Telegram users
   - Uses matching algorithm to find best fits

---

## 🧪 Testing

### Test the Scraper
```bash
uv run python test_scraper.py
```

### Test Email Sending
1. Install Mailpit: `curl -sL https://raw.githubusercontent.com/axllent/mailpit/develop/install.sh | sh`
2. Run Mailpit: `mailpit`
3. Visit http://localhost:8025 to view emails

### Test Telegram Bot
```bash
uv run python run_bot.py
```

---

## 🌍 Internationalization

All system messages, logs, and notifications are in **English** for international deployment.

---

## 🔒 Security Considerations

- **Change SECRET_KEY** in `.env` before production deployment
- **Change admin password** in `app/main.py` (AdminAuth class)
- **Use HTTPS** in production
- **Enable rate limiting** (already configured: 60 req/min)
- **Use PostgreSQL** instead of SQLite for production
- **Set up proper email provider** (e.g., SendGrid, AWS SES)

---

## 📈 Future Enhancements

- [ ] PostgreSQL database support
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Advanced matching algorithm with ML
- [ ] User profile pictures
- [ ] Job application tracking
- [ ] Company profiles
- [ ] Salary range filtering
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Pouriya**
- GitHub: [@pouriya-py](https://github.com/pouriya-py)

---

## 🙏 Acknowledgments

- Job data sourced from: Remotive, WeWorkRemotely, RemoteOK, Python.org, Hacker News
- Built with FastAPI, SQLAlchemy, and Aiogram
- UI inspired by modern dark theme designs

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star on GitHub! ⭐**

</div>
```

