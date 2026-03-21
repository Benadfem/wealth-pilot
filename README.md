# 💰 Wealth-Pilot

A production-grade AI-powered financial API
built with FastAPI, PostgreSQL and LangGraph.

## 🌍 Live Demo
**https://wealth-pilot.onrender.com**

## 🤖 Ask the AI Agent
- "How much have I spent on food?"
- "What should I do to prevent overspending?"
- "Show me all my transactions"

## 🛠️ Tech Stack
| Technology | Purpose |
|------------|---------|
| FastAPI | REST API framework |
| PostgreSQL | Persistent database |
| SQLAlchemy | Database ORM |
| JWT | Secure authentication |
| Async Python | Production performance |
| LangGraph | AI Agent framework |
| Groq + Llama | AI brain |
| Render | Cloud deployment |

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /register | Create account |
| POST | /login | Get JWT token |
| GET | /transactions | View transactions |
| POST | /transactions | Add transaction |
| POST | /agent | Ask the AI |

## 🚀 Run Locally
```bash
git clone https://github.com/Benadfem/wealth-pilot.git
cd wealth-pilot
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 👨‍💻 Author
**Adedoyin Benson**
- GitHub: [@Benadfem](https://github.com/Benadfem)
- LinkedIn: [Adedoyin Benson](https://linkedin.com/in/adedara-adedoyin)
- Live App: [wealth-pilot.onrender.com](https://wealth-pilot.onrender.com)
