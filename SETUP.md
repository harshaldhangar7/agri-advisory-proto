# Setup and Usage Guide

## Project Structure

```
agri-advisory-proto/
├── backend/
│   ├── app/
│   │   ├── db.py              # Database configuration
│   │   ├── init_db.py         # Database initialization
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── models.py          # SQLModel schemas
│   │   ├── utils.py           # Utilities (auth, response helpers)
│   │   ├── seed.py            # Sample data seeding
│   │   └── routers/
│   │       ├── farmers.py     # Farmer CRUD endpoints
│   │       └── advisory.py    # Advisory recommendation endpoints
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── styles.css
│       └── components/
│           ├── FarmerForm.jsx      # Create farmer form
│           ├── FarmerList.jsx      # List and manage farmers
│           └── AdvisoryPanel.jsx   # Get agricultural advice
├── setup_database.py          # Automatic database setup script ⭐
├── .env                        # Environment configuration
├── .env.example               # Example environment file
├── SETUP.md                   # Setup guide
└── README.md
```

## Prerequisites

- **Python 3.10+** (in PATH)
- **Node.js 18+** and npm
- **MySQL Server** installed and running
- **PowerShell** (on Windows)

## Backend Setup

### 1. Automatic Database Setup (Recommended) ⭐

This script handles everything automatically - no manual MySQL commands needed!

**First, install dependencies:**

```bash
cd backend
pip install -r requirements.txt
cd ..
```

**Configure environment:**

Create `.env` file in the project root (copy from `.env.example`):

```bash
# Database Configuration
DATABASE_URL=mysql+pymysql://agriuser:your_password@localhost:3306/agri?charset=utf8mb4

# MySQL Root Password (for setup script)
DATABASE_ROOT_PASS=root_password

# API Security
API_KEY=default-dev-key

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
FRONTEND_URL=http://localhost:5173
```

**Run automated setup:**

```bash
# Ensure MySQL is running, then run:
python setup_database.py
```

This script will:
- ✅ Connect to MySQL as root
- ✅ Create the database (`agri`)
- ✅ Create the database user (`agriuser`)
- ✅ Grant all privileges
- ✅ Create all tables
- ✅ Optionally seed sample data
- ✅ Verify everything works

Done! The database is ready. Skip to "Start Backend Server" below.

---

### 2. Manual Database Setup (Alternative)

If you prefer to set up manually or `setup_database.py` has issues:

Open MySQL Shell or Workbench and run:

```sql
CREATE DATABASE agri CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'agriuser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON agri.* TO 'agriuser'@'localhost';
FLUSH PRIVILEGES;
```

Then initialize tables:

```bash
cd backend/app
python init_db.py
cd ../..
```

---

### 3. Install Python Dependencies (if not done)

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 4. Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**API Documentation**: Visit `http://localhost:8000/docs` for interactive Swagger UI

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

All endpoints require `X-API-Key` header with the API key from `.env`

### Farmers Management

- `GET /api/farmers/` - List all farmers
- `POST /api/farmers/` - Create a new farmer
- `GET /api/farmers/{farmer_id}` - Get farmer details with plots
- `PUT /api/farmers/{farmer_id}` - Update farmer information
- `DELETE /api/farmers/{farmer_id}` - Delete a farmer
- `POST /api/farmers/{farmer_id}/plots` - Add a plot to farmer
- `GET /api/farmers/{farmer_id}/plots` - Get all plots for a farmer
- `DELETE /api/farmers/{farmer_id}/plots/{plot_id}` - Delete a plot

### Advisory

- `POST /api/advisory/recommend` - Get agricultural advisory for a plot

### Health

- `GET /health` - Health check endpoint

## Features

### Phase 1: Core
✅ Database schema with Farmer and Plot models
✅ FastAPI backend with CORS enabled
✅ Frontend UI with Vite and React
✅ Basic farmer creation and advisory recommendations

### Phase 2: Security & Validation
✅ API key authentication on all endpoints
✅ Input validation with Pydantic validators
✅ Environment variable configuration
✅ Error handling and logging
✅ Frontend form validation

### Phase 3: Complete CRUD & Enhanced UX
✅ Complete farmer CRUD operations (Create, Read, Update, Delete)
✅ Plot management (Add, View, Delete)
✅ Logging system
✅ Improved frontend styling
✅ Farmer list with search and management
✅ API proxy configuration for Vite
✅ Responsive UI design

## Running Complete System

**First time setup:**

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt
cd ..

cd frontend
npm install
cd ..

# 2. Configure .env (copy from .env.example and update DATABASE_URL)

# 3. Setup database (handles creation, user, tables, sample data)
python setup_database.py
```

**Running the application:**

### Terminal 1: Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.

## Testing the API

### Using Curl

```bash
# List farmers
curl -H "x-api-key: your-api-key" http://localhost:8000/api/farmers/

# Create farmer
curl -X POST -H "Content-Type: application/json" -H "x-api-key: your-api-key" \
  -d '{"name":"Ram","phone":"+919876543210","language":"mr"}' \
  http://localhost:8000/api/farmers/

# Get advisory
curl -X POST -H "Content-Type: application/json" -H "x-api-key: your-api-key" \
  -d '{"plot_id":"plot-id-here","symptoms":"yellow leaves","weather":{"rain_last_3_days":10}}' \
  http://localhost:8000/api/advisory/recommend
```

### Using Swagger UI

1. Start the backend server
2. Open `http://localhost:8000/docs`
3. Click "Authorize" and enter your API key
4. Try out endpoints interactively

## Production Deployment

1. **Change API_KEY**: Update to a strong random string in `.env`
2. **Database**: Use managed database service (AWS RDS, Azure Database, etc.)
3. **Frontend Build**: `npm run build` in frontend directory
4. **Serve Static Files**: Configure FastAPI to serve built frontend
5. **HTTPS**: Enable SSL/TLS certificates
6. **Logging**: Configure external logging service (Sentry, CloudWatch, etc.)
7. **Rate Limiting**: Add rate limiting middleware for API protection

## Troubleshooting

### Setup Script Errors (setup_database.py)

#### "Could not connect to MySQL as root"
- Ensure MySQL server is running
- Check if root password is needed: Set `DATABASE_ROOT_PASS=your_root_password` in `.env`
- On Windows, MySQL might not be in PATH - start MySQL from Services

#### "Missing required package"
- Run: `pip install -r backend/requirements.txt`

#### "DATABASE_URL not set"
- Create `.env` file (copy from `.env.example`)
- Set correct DATABASE_URL with your credentials

#### "Permission denied" or "Access denied"
- Ensure DATABASE_URL has correct username and password
- Check DATABASE_ROOT_PASS is correct
- MySQL user might already exist - script handles this automatically

### Database Connection Error
- Check MySQL server is running
- Verify DATABASE_URL in `.env` is correct
- Ensure user and database exist in MySQL

### CORS Errors
- Verify FRONTEND_URL in `.env` matches your frontend URL
- Check API_KEY header is being sent in requests

### API Key Errors
- Ensure `x-api-key` header is included in all API requests
- Verify API_KEY value matches in `.env`

### Frontend Not Connecting to API
- Check vite.config.js API proxy is configured
- Verify backend server is running on port 8000
- Check browser console for CORS errors

## Logging

Backend logs are printed to console with timestamps and log levels:
- `INFO`: General application events
- `WARNING`: Potential issues
- `ERROR`: Application errors
- `DEBUG`: Detailed debugging information (health checks)

To view logs in production, configure:
- File logging: Update logging config in `main.py`
- External service: Integrate Sentry, CloudWatch, etc.

## Contributing

1. Create branches for new features: `git checkout -b feature/name`
2. Follow PEP 8 for Python code
3. Update models in `models.py` and add migrations if needed
4. Add validation for new fields
5. Test endpoints with Swagger UI before committing

## License

MIT License - See LICENSE file for details
