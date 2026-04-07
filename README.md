# Agri Advisory Prototype

Smart agricultural advisory system for farmers with web-based farmer management and crop recommendations.

## 🚀 Quick Start

**Get running in 3 steps!** See [QUICKSTART.md](QUICKSTART.md) for a fast setup guide.

```bash
# 1. Install dependencies
pip install -r backend/requirements.txt
npm install --prefix frontend

# 2. Configure environment (.env file)
cp .env.example .env
# Edit .env with your database credentials

# 3. Setup database (automatic!)
python setup_database.py

# 4. Run application
# Terminal 1: cd backend && python -m uvicorn app.main:app --reload
# Terminal 2: cd frontend && npm run dev
# Open: http://localhost:5173
```

---

## 📋 Features

✅ **Farmer Management**
- Create, read, update, delete farmers
- Manage multiple plots per farmer
- View farmer details and associated plots

✅ **Agricultural Advisory**
- Get smart recommendations based on crop symptoms
- Weather impact analysis
- Symptom-based crop health diagnosis

✅ **Security & Authentication**
- API key protection on all endpoints
- Input validation and error handling
- Environment-based configuration

✅ **Professional UI**
- Responsive React frontend with Vite
- Modern styling with CSS
- Real-time feedback and error messages
- Interactive farmer list management

✅ **Production Ready**
- Comprehensive logging system
- Error tracking and reporting
- Swagger API documentation (`/docs`)
- Database with SQLModel ORM

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** ⭐ - Fast 5-minute setup guide
- **[SETUP.md](SETUP.md)** - Detailed setup and troubleshooting
- **[API Docs](http://localhost:8000/docs)** - Interactive Swagger UI (after running backend)

---

## 🛠️ Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLModel - SQL database ORM
- Uvicorn - ASGI server
- MySQL - Database

**Frontend:**
- React 18 - UI library
- Vite - Build tool
- Axios - HTTP client

---

## 📁 Project Structure

```
agri-advisory-proto/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── models.py            # Database models
│   │   ├── db.py                # Database config
│   │   ├── utils.py             # Auth & helpers
│   │   └── routers/
│   │       ├── farmers.py       # Farmer endpoints
│   │       └── advisory.py      # Advisory endpoints
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/          # React components
│   │   └── styles.css
│   └── package.json
├── setup_database.py            # Automatic DB setup ⭐
├── .env.example                 # Configuration template
├── QUICKSTART.md                # Quick setup guide
└── SETUP.md                     # Detailed guide
```

---

## 🔧 Development

### Environment Setup

Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

Update with your configuration:
```env
DATABASE_URL=mysql+pymysql://agriuser:password@localhost:3306/agri?charset=utf8mb4
DATABASE_ROOT_PASS=root_password
API_KEY=your-api-key
FRONTEND_URL=http://localhost:5173
```

### Automatic Database Setup

```bash
python setup_database.py
```

Handles:
- Database creation
- User creation
- Table initialization
- Optional sample data

### Running Locally

**Backend** (Terminal 1):
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

Access at: `http://localhost:5173`

---

## 📖 API Endpoints

All endpoints require `X-API-Key` header.

**Farmers:**
- `GET /api/farmers/` - List all farmers
- `POST /api/farmers/` - Create farmer
- `GET /api/farmers/{id}` - Get farmer details
- `PUT /api/farmers/{id}` - Update farmer
- `DELETE /api/farmers/{id}` - Delete farmer
- `POST /api/farmers/{id}/plots` - Add plot
- `GET /api/farmers/{id}/plots` - List plots
- `DELETE /api/farmers/{id}/plots/{plot_id}` - Delete plot

**Advisory:**
- `POST /api/advisory/recommend` - Get crop advice

**Health:**
- `GET /health` - Health check

See [SETUP.md](SETUP.md#api-endpoints) for full documentation.

---

## 🐛 Troubleshooting

**Database connection error?**
- Ensure MySQL is running
- Check DATABASE_URL in .env
- Run: `python setup_database.py`

**API not connecting from frontend?**
- Verify backend running on port 8000
- Check `FRONTEND_URL` in .env
- Clear browser cache

**Sample data not loading?**
- Run setup again: `python setup_database.py`
- Select "y" when asked to seed data

See [SETUP.md](SETUP.md#troubleshooting) for more troubleshooting.

---

## 📦 Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **MySQL 5.7+** or **MariaDB**
- Windows/Mac/Linux

---

## 🚀 Deployment

For production:

1. Update `API_KEY` to strong random value
2. Use managed database (AWS RDS, Azure Database, etc.)
3. Build frontend: `npm run build`
4. Configure HTTPS/SSL
5. Set up logging service (Sentry, CloudWatch, etc.)
6. Add rate limiting
7. Use production-grade web server (Gunicorn, Nginx)

See [SETUP.md#production-deployment](SETUP.md#production-deployment) for details.

---

## 📝 License

MIT License - Free to use and modify

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Ready to start?** Go to [QUICKSTART.md](QUICKSTART.md) now! 🌾