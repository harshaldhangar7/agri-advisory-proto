# 🌾 Agri Advisory Prototype

A modern agricultural management system with smart advisory recommendations, farmer management, and secure JWT-based authentication.

## ✨ Key Features

### 🔐 Authentication & Security
- ✅ JWT (JSON Web Token) authentication system
- ✅ User registration and login with password hashing
- ✅ Argon2 secure password hashing (no weak password limits)
- ✅ Access tokens (30 min) + Refresh tokens (7 days)
- ✅ Automatic token refresh with axios interceptors
- ✅ Password recovery with time-limited reset codes
- ✅ Protected routes and API endpoints
- ✅ User-isolated data access

### 👨‍🌾 Farmer Management
- ✅ Create, read, update, delete farmers
- ✅ Manage multiple plots per farmer
- ✅ View farmer details and associated plots
- ✅ Farmer search and filtering
- ✅ Farmer-specific data (name, phone, language preference)

### 🌱 Agricultural Advisory
- ✅ Smart crop recommendations based on symptoms
- ✅ Weather impact analysis
- ✅ Symptom-based crop health diagnosis
- ✅ Real-time advisory panel

### 🎨 Professional UI
- ✅ Modern React frontend with Vite
- ✅ Responsive design with CSS
- ✅ Real-time feedback and error messages
- ✅ Login/Registration page with form validation
- ✅ User dashboard with logout
- ✅ Protected routes (requires authentication)
- ✅ Interactive farmer list management
- ✅ Plot management interface

### 📊 Production Ready
- ✅ Comprehensive logging system
- ✅ Error handling and tracking
- ✅ Swagger API documentation (`/docs`)
- ✅ SQLModel ORM with MySQL
- ✅ CORS support
- ✅ Environment-based configuration

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- MySQL 5.7+ (local or remote)
- Git

### Setup Steps

```bash
# 1. Clone and navigate to project
cd agri-advisory-proto

# 2. Create environment file
cp .env.example .env
# Edit .env with your MySQL credentials

# 3. Create Python virtual environment
python -m venv venv
# Activate: 
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 4. Install dependencies
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..

# 5. Initialize database
python -c "from backend.app.db import init_db; init_db(); print('✅ Database initialized!')"

# 6. Start backend (Terminal 1)
cd backend
python -m uvicorn app.main:app --reload --port 8000

# 7. Start frontend (Terminal 2)
cd frontend
npm run dev

# 8. Open browser
# Visit: http://localhost:5173
# Login with any credentials (auto-register on first login)
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | FastAPI | Modern async web framework |
| | Python 3.10+ | Server language |
| | SQLModel | ORM with SQLAlchemy |
| | PyJWT | JWT token generation |
| | Argon2-cffi | Secure password hashing |
| | Passlib | Password context management |
| **Database** | MySQL 5.7+ | Relational data storage |
| **Frontend** | React 18 | UI library |
| | Vite | Build tool & dev server |
| | Axios | HTTP client with interceptors |
| | React Context | State management |
| **Deployment** | Docker | Containerization |
| | Gunicorn | Production WSGI server |
| | Nginx | Reverse proxy |

---

## 📁 Project Structure

```
agri-advisory-proto/
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI app entry point
│   │   ├── db.py                        # Database configuration
│   │   ├── models.py                    # SQLModel database models
│   │   ├── auth.py                      # JWT & password utilities ⭐
│   │   ├── init_db.py                   # Database initialization
│   │   ├── seed.py                      # Sample data
│   │   └── routers/
│   │       ├── auth.py                  # Authentication endpoints ⭐
│   │       ├── farmers.py               # Farmer management endpoints
│   │       └── advisory.py              # Advisory recommendations
│   └── requirements.txt                 # Python dependencies
│
├── frontend/
│   ├── public/                          # Static assets
│   ├── src/
│   │   ├── main.jsx                     # React entry point
│   │   ├── App.jsx                      # Root component
│   │   ├── styles.css                   # Global styles
│   │   ├── pages/
│   │   │   └── LoginPage.jsx            # Login/Register/Forgot Password ⭐
│   │   ├── context/
│   │   │   └── AuthContext.jsx          # Authentication state ⭐
│   │   └── components/
│   │       ├── FarmerForm.jsx           # Create/edit farmer form
│   │       ├── FarmerList.jsx           # List farmers
│   │       ├── PlotForm.jsx             # Plot management
│   │       └── AdvisoryPanel.jsx        # Advisory recommendations
│   ├── package.json
│   ├── vite.config.js
│   └── LoginPage.css                    # Login page styling
│
├── docs/
│   ├── JWT_AUTHENTICATION.md            # JWT implementation details
│   ├── FRONTEND_IMPLEMENTATION.md       # Frontend architecture
│   ├── JWT_QUICK_START.md              # Quick JWT guide
│   └── FORGOT_PASSWORD_FEATURE.md       # Password recovery docs ⭐
│
├── .env.example                         # Environment template
├── .env                                 # Local config (create from .env.example)
├── README.md                            # This file
└── agri-advisory-proto.code-workspace  # VS Code workspace config
```

---

## 🏃 Running Guides by Environment

### 1️⃣ Development (Local Environment)

**Best for:** Development and testing

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend  
cd frontend
npm run dev

# Results:
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

**Environment file (.env):**
```env
DATABASE_URL=mysql+pymysql://agriuser:password@localhost:3306/agri?charset=utf8mb4
SECRET_KEY=your-dev-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 2️⃣ Production (Gunicorn + Nginx)

**Best for:** Production deployment on Linux servers

```bash
# 1. Install production dependencies
pip install -r backend/requirements.txt gunicorn

# 2. Build frontend
cd frontend
npm run build
# Output: frontend/dist/

# 3. Start backend with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:8000 backend.app.main:app

# 4. Configure Nginx
# Point to backend on :8000 and frontend dist on /
# See nginx.conf.example below
```

**Nginx Configuration (nginx.conf):**
```nginx
upstream api_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    # Frontend static files
    location / {
        root /var/www/agri-advisory/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API backend
    location /api {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Environment file (.env):**
```env
DATABASE_URL=mysql+pymysql://agriuser:securepass@db.example.com:3306/agri?charset=utf8mb4
SECRET_KEY=generate-with-secrets.token_urlsafe()
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3️⃣ Docker (Containerized)

**Best for:** Consistent environments across machines

**Build and run:**
```bash
# Build image
docker build -t agri-advisory .

# Run container with MySQL
docker run -d \
  --name agri-app \
  -p 8000:8000 \
  -p 5173:5173 \
  -e DATABASE_URL=mysql+pymysql://user:pass@mysql-host:3306/agri \
  -e SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe())") \
  agri-advisory

# Check logs
docker logs agri-app
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim as backend

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt gunicorn

COPY backend ./backend

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "backend.app.main:app"]
```

### 4️⃣ Docker Compose (Full Stack)

**Best for:** Complete standalone deployment

```bash
# Start all services
docker-compose up -d

# Monitor logs
docker-compose logs -f

# Stop services
docker-compose down
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: agri
      MYSQL_USER: agriuser
      MYSQL_PASSWORD: agripass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  backend:
    build: ./
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://agriuser:agripass@mysql:3306/agri
      SECRET_KEY: your-secret-key-here
    depends_on:
      - mysql

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:5173"

volumes:
  mysql_data:
```

### 5️⃣ Cloud Platforms

#### **Heroku:**
```bash
# Login and create app
heroku login
heroku create agri-advisory

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

#### **AWS Elastic Beanstalk:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init
eb create agri-advisory-env
eb open  # Opens in browser
```

#### **DigitalOcean App Platform:**
- Connect GitHub repo
- Auto-deploy on push
- Set environment variables in UI
- Managed database available

---

## 🔐 Authentication System

### Login/Register Flow

```
User → LoginPage → Register/Login → JWT Tokens → Dashboard
                     ↓
              Password Reset Option
              (Forgot Password)
```

### JWT Token Structure

**Access Token (30 minutes):**
```json
{
  "sub": "user_id",
  "exp": 1234567890,
  "type": "access",
  "iat": 1234567800
}
```

**Refresh Token (7 days):**
```json
{
  "sub": "user_id",
  "exp": 1234999099,
  "type": "refresh",
  "iat": 1234567800
}
```

### API Authentication

All protected endpoints require `Authorization` header:

```bash
curl -H "Authorization: Bearer {access_token}" \
     http://localhost:8000/api/farmers/
```

Tokens auto-refresh via axios interceptors on the frontend.

---

## 📚 API Endpoints

### Authentication Routes

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Create new account | ❌ |
| POST | `/api/auth/login` | Login with credentials | ❌ |
| POST | `/api/auth/refresh` | Refresh access token | ❌ |
| POST | `/api/auth/forgot-password` | Request password reset | ❌ |
| POST | `/api/auth/reset-password` | Reset password with code | ❌ |
| GET | `/api/auth/me` | Get current user | ✅ |
| POST | `/api/auth/logout` | Logout (client-side) | ✅ |

### Farmer Routes

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/farmers/` | List all farmers | ✅ |
| POST | `/api/farmers/` | Create new farmer | ✅ |
| GET | `/api/farmers/{id}` | Get farmer details | ✅ |
| PUT | `/api/farmers/{id}` | Update farmer | ✅ |
| DELETE | `/api/farmers/{id}` | Delete farmer | ✅ |
| GET | `/api/farmers/{id}/plots` | Get farmer's plots | ✅ |
| POST | `/api/farmers/{id}/plots` | Add plot to farmer | ✅ |
| DELETE | `/api/farmers/{id}/plots/{plot_id}` | Delete plot | ✅ |

### Advisory Routes

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/advisory/recommend` | Get crop recommendation | ✅ |

### Documentation

- **Interactive API Docs:** `http://localhost:8000/docs` (Swagger UI)
- **ReDoc:** `http://localhost:8000/redoc` (Alternative documentation)

---

## 🔄 Database Schema

### User Table
```sql
CREATE TABLE user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(500) NOT NULL,
  reset_code VARCHAR(255),
  reset_code_expiry VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Farmer Table
```sql
CREATE TABLE farmer (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  language VARCHAR(10) DEFAULT 'mr',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Plot Table
```sql
CREATE TABLE plot (
  id INT PRIMARY KEY AUTO_INCREMENT,
  farmer_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  area_hectares FLOAT NOT NULL,
  crop VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (farmer_id) REFERENCES farmer(id)
);
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```env
# Database
DATABASE_URL=mysql+pymysql://agriuser:password@localhost:3306/agri?charset=utf8mb4

# JWT  
SECRET_KEY=your-secret-key-here-generate-with-secrets.token_urlsafe()
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend
FRONTEND_URL=http://localhost:5173
```

### Security Best Practices

✅ Generate strong SECRET_KEY:
```python
import secrets
print(secrets.token_urlsafe(32))
```

✅ Use HTTPS in production
✅ Set secure CORS origins
✅ Use strong database passwords
✅ Enable rate limiting
✅ Monitor logs for suspicious activity

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Database connection error | Check DATABASE_URL, ensure MySQL running |
| Port 8000 already in use | Change port: `uvicorn ... --port 8001` |
| Frontend can't reach API | Check backend is running, verify localhost:8000 |
| 401 Unauthorized errors | Tokens expired, refresh or re-login |
| CORS errors | Verify CORS origins in backend/app/main.py |
| Database not initialized | Run: `python -c "from backend.app.db import init_db; init_db()"` |

### Common Errors

**`ModuleNotFoundError: No module named 'backend'`**
```bash
# Ensure you're in project root (agri-advisory-proto)
cd agri-advisory-proto
```

**`MySQL connection refused`**
```bash
# Check MySQL is running
mysql -u root -p  # Test connection
# Or use Docker: docker run -d -p 3306:3306 mysql:8.0
```

**`npm ERR! 404`**
```bash
# Clean and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📖 Documentation Files

Detailed documentation available in `/docs`:

- **[JWT_AUTHENTICATION.md](docs/JWT_AUTHENTICATION.md)** - Complete JWT implementation
- **[FRONTEND_IMPLEMENTATION.md](docs/FRONTEND_IMPLEMENTATION.md)** - React architecture
- **[JWT_QUICK_START.md](docs/JWT_QUICK_START.md)** - Quick JWT reference
- **[FORGOT_PASSWORD_FEATURE.md](docs/FORGOT_PASSWORD_FEATURE.md)** - Password recovery details

---

## 🧪 Testing

### Test Password Recovery
```bash
python test_forgot_password.py
```

### Test API Endpoints
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user@example.com","password":"Pass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"Pass123"}'

# Get farmers (requires token)
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/farmers/
```

---

## 📦 Deployment Checklist

- [ ] Update SECRET_KEY to strong random value
- [ ] Set DATABASE_URL to production database
- [ ] Enable HTTPS/SSL certificate
- [ ] Configure CORS origins
- [ ] Set up monitoring and logging
- [ ] Enable database backups
- [ ] Configure email for password resets
- [ ] Set up CDN for static files
- [ ] Enable rate limiting
- [ ] Test all endpoints
- [ ] Set up automated backups
- [ ] Configure health check endpoints

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/name`
3. Make changes and test
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature/name`
6. Create pull request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🆘 Support

- 📧 Email: support@example.com (Replace with actual)
- 🐛 Report issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Email notifications for password reset
- [ ] Two-factor authentication (2FA)
- [ ] Role-based access control (admin/user)
- [ ] Advanced analytics dashboard
- [ ] Weather API integration
- [ ] SMS notifications
- [ ] Multi-language support

---

**Ready to start?**

```bash
cd agri-advisory-proto
cp .env.example .env
# Edit .env with your credentials
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
# Terminal 1: cd backend && python -m uvicorn app.main:app --reload
# Terminal 2: cd frontend && npm run dev
# Open: http://localhost:5173
```

🌾 Happy farming!