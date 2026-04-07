# JWT Authentication System - Quick Start Guide

Complete guide to run the Agri Advisory application with JWT authentication.

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- MySQL server running
- Git (optional)

## Step 1: Backend Setup (5 minutes)

### 1a. Navigate to backend directory
```bash
cd backend
```

### 1b. Create Python virtual environment
```powershell
# On Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# On CMD
python -m venv venv
venv\Scripts\activate.bat

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 1c. Install dependencies
```bash
pip install -r requirements.txt
```

### 1d. Initialize database
From the project root directory (agri-advisory-proto):
```bash
python backend/app/init_db.py
```

**When prompted**, enter MySQL root password: `harshal`

This will:
- ✅ Create `agri` database
- ✅ Create `agriuser` MySQL user
- ✅ Create all tables including User table
- ✅ Insert sample data

### 1e. Verify environment variables
Check `.env` file in project root:
```env
DATABASE_URL=mysql+pymysql://agriuser:harshal@localhost:3306/agri?charset=utf8mb4
SECRET_KEY=your-secret-key-change-in-production-please-use-a-long-random-string
APP_HOST=0.0.0.0
APP_PORT=8000
FRONTEND_URL=http://localhost:5173
```

**Important**: For production, change `SECRET_KEY` to a long random string!

## Step 2: Frontend Setup (3 minutes)

### 2a. Navigate to frontend directory
```bash
cd frontend
```

### 2b. Install dependencies
```bash
npm install
```

### 2c. Create .env file (if needed)
Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

## Step 3: Run the Application (2 minutes)

### Option A: Run in Two Terminal Windows (Recommended)

**Terminal 1 - Backend:**
```bash
cd agri-advisory-proto
.\backend\venv\Scripts\Activate.ps1  # Windows PowerShell
python backend/app/main.py
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd agri-advisory-proto/frontend
npm run dev
```

Expected output:
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Option B: Run Sequentially (For Testing)

```bash
# Terminal 1: Start backend
cd agri-advisory-proto
python backend/app/main.py

# Wait for "Application startup complete" message

# Terminal 2: Start frontend (new terminal/new cmd window)
cd agri-advisory-proto/frontend
npm run dev

# Open browser to http://localhost:5173
```

## Step 4: Test the System (3 minutes)

### 4a. Open in Browser
1. Go to http://localhost:5173
2. You should see the login page with:
   - Login tab (default)
   - Username/password form
   - "Register" link at the bottom

### 4b. Create New User (Register)
1. Click "Register" at the bottom
2. Enter:
   - Username: `testfarmer1`
   - Email: `testfarmer1@example.com`
   - Password: `Test@1234`
   - Confirm Password: `Test@1234`
3. Click "Register" button
4. You should see:
   - ✅ "Welcome, testfarmer1!" in header
   - ✅ "Logout" button appears
   - ✅ Main dashboard with forms visible

### 4c. Test Farmer Operations
1. **Create Farmer**
   - Name: `John Doe`
   - Phone: `9876543210`
   - Click "Create Farmer"
   - Should see success message with ID

2. **View Farmers**
   - Click "Refresh" in Farmers List section
   - Should see your created farmer

3. **Add Plot**
   - Click "View" next to farmer
   - Fill plot form:
     - Plot Name: `Field A`
     - Crop: `Wheat`
     - Area: `5.5` hectares
   - Click "Add Plot"
   - Should see success message

4. **Get Advisory**
   - Enter plot ID (should be `1` if first plot)
   - Click "Get Advice"
   - Should see agricultural recommendations

### 4d. Test Authentication
1. **Refresh Page** - You should stay logged in (token in localStorage)
2. **Logout** - Click logout, should return to login page
3. **Login Again** - Use `testfarmer1` / `Test@1234`
4. **Wrong Password** - Try login with wrong password, should show error

## Complete Test Checklist

- [ ] Registration works
- [ ] Login works with correct credentials
- [ ] Wrong credentials show error
- [ ] User stays logged in after refresh
- [ ] User name displays in header
- [ ] Logout clears authentication
- [ ] Can create farmer after login
- [ ] Can view farmer list after login
- [ ] Can add plot to farmer
- [ ] Can get advisory for plot
- [ ] All delete operations work
- [ ] Error messages display properly
- [ ] Loading states work correctly

## Troubleshooting

### "Connection refused" on localhost:8000
**Solution:**
- Ensure backend is running: `python backend/app/main.py`
- Check terminal doesn't show errors
- Verify port 8000 is not in use: `netstat -ano | findstr :8000`

### "Cannot find module" error in frontend
**Solution:**
```bash
cd frontend
npm install
npm run dev
```

### "DATABASE_URL not set" error
**Solution:**
- Ensure `.env` exists in project root
- Contains: `DATABASE_URL=mysql+pymysql://...`
- Run: `python backend/app/init_db.py`

### MySQL connection error
**Solution:**
- Start MySQL service
- Verify root password in `.env` (should be `harshal`)
- Check MySQL is on port 3306
- Run: `python backend/app/init_db.py`

### "Port 8000 already in use"
**Solution:**
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace 12345 with PID shown above)
taskkill /PID 12345 /F

# Try again
python backend/app/main.py
```

### "Port 5173 already in use"
**Solution:**
```bash
# Kill process on port 5173
# On macOS/Linux: lsof -ti:5173 | xargs kill -9
# Or just use different port
npm run dev -- --port 5174
```

### Black screen or "Loading..." forever
**Solution:**
- Check browser console (F12) for errors
- Check network tab for failed requests
- Verify backend is running and accessible
- Check CORS configuration in `backend/app/main.py`

### Tokens not persisting after refresh
**Solution:**
- Check browser localStorage (F12 > Application > Local Storage)
- Should see: `access_token`, `refresh_token`, `user`
- If empty, registration/login not working
- Check browser console for errors

## API Endpoints Reference

### Authentication Endpoints
```
POST /api/auth/register          - Register new user
POST /api/auth/login             - Login user
POST /api/auth/refresh           - Refresh access token
GET  /api/auth/me                - Get current user
POST /api/auth/logout            - Logout user
```

### Farmer Endpoints (require JWT)
```
GET    /api/farmers/             - List all farmers
POST   /api/farmers/             - Create farmer
GET    /api/farmers/{id}         - Get farmer details
PUT    /api/farmers/{id}         - Update farmer
DELETE /api/farmers/{id}         - Delete farmer
```

### Plot Endpoints (require JWT)
```
POST   /api/farmers/{id}/plots   - Add plot
GET    /api/farmers/{id}/plots   - Get farmer's plots
DELETE /api/farmers/{id}/plots/{pid} - Delete plot
```

### Advisory Endpoint (requires JWT)
```
POST   /api/advisory/recommend   - Get advisory
```

## Example API Calls with cURL

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test@1234"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test@1234"
  }'
```

### Get Farmers (using token from login response)
```bash
curl -X GET http://localhost:8000/api/farmers/ \
  -H "Authorization: Bearer <your_access_token>"
```

## Environment Setup Reference

### Windows Terminal Setup
```powershell
# One-time setup:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# For each session:
#   Terminal 1 - Backend
cd C:\path\to\agri-advisory-proto
.\backend\venv\Scripts\Activate.ps1
python backend/app/main.py

#   Terminal 2 - Frontend
cd C:\path\to\agri-advisory-proto\frontend
npm run dev
```

### macOS/Linux Terminal Setup
```bash
# Terminal 1 - Backend
cd ~/path/to/agri-advisory-proto
source backend/venv/bin/activate
python backend/app/main.py

# Terminal 2 - Frontend
cd ~/path/to/agri-advisory-proto/frontend
npm run dev
```

## Next Steps

1. **Review Implementation**
   - [JWT_AUTHENTICATION.md](./JWT_AUTHENTICATION.md) - Complete system design
   - [FRONTEND_IMPLEMENTATION.md](./FRONTEND_IMPLEMENTATION.md) - Frontend details
   - [SETUP.md](./SETUP.md) - Detailed setup guide

2. **Production Deployment**
   - Change `SECRET_KEY` to random strong string
   - Update `FRONTEND_URL` to production domain
   - Enable HTTPS
   - Set up proper logging
   - Configure database backups

3. **Add Features**
   - Password reset flow
   - User profile page
   - Role-based access control
   - Multi-factor authentication
   - Session management

4. **Security Hardening**
   - Add rate limiting on auth endpoints
   - Implement CSRF protection
   - Token rotation on refresh
   - Logout blacklist
   - httpOnly cookies for tokens

## Quick Commands Reference

```bash
# Start fresh
cd agri-advisory-proto

# Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..
python backend/app/init_db.py
python backend/app/main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Open browser
# http://localhost:5173
```

## Support

**For issues, check:**
1. Backend logs in terminal
2. Frontend console (F12)
3. Network tab for API errors
4. Database connection with `python backend/app/init_db.py`
5. Environment variables in `.env`

**Common errors:**
- 401: Token invalid or missing - Re-login
- 422: Validation error - Check form inputs
- 500: Server error - Check backend logs
- CORS error - Verify FRONTEND_URL in .env
- MySQL error - Verify database is running

## Success Indicators

✅ You've successfully set up JWT authentication when:
- User registration works without API key
- Login returns access and refresh tokens
- Can perform CRUD operations with JWT
- User stays logged in after page refresh
- Logout clears authentication
- Token automatically refreshes when expired
- All components show user name in header

Happy farming! 🌾
