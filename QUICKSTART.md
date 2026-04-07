# Quick Start Guide - Agri Advisory Prototype

Get the project running in **3 simple steps**! 🚀

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
# Install Python packages
cd backend
pip install -r requirements.txt
cd ..

# Install Node packages
cd frontend
npm install
cd ..
```

### Step 2: Configure Environment

Create `.env` file in project root:

```bash
# Edit .env with your database details:
# Copy from .env.example and update:

DATABASE_URL=mysql+pymysql://agriuser:your_password@localhost:3306/agri?charset=utf8mb4
DATABASE_ROOT_PASS=root_password_or_empty
API_KEY=default-dev-key
```

### Step 3: Setup Database (Automatic) ⭐

```bash
# One command - handles everything!
python setup_database.py
```

**This script automatically:**
- ✅ Creates MySQL database
- ✅ Creates database user  
- ✅ Sets up all tables
- ✅ Seeds sample data (optional)
- ✅ Verifies everything works

---

## ▶️ Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open browser:** http://localhost:5173 🎉

---

## 🧪 Test It Out

### Create a Farmer
1. Fill in "Create Farmer" form
2. Enter name + phone
3. Click "Create"
4. See farmer appear in "Farmers List"

### Get Advisory
1. Copy a Plot ID from the farmer details
2. Go to "Get Advisory" section
3. Paste Plot ID and describe symptoms
4. Click "Get Advice" to see recommendations

### Manage Farmers
1. View all farmers in "Farmers List"
2. Click "View" to see details and plots
3. Click "Delete" to remove a farmer

---

## 🐛 If Something Goes Wrong

### Database Issues
**Error: "Could not connect to MySQL as root"**
```bash
# Make sure MySQL is running
# On Windows: Open Services and start MySQL
# Check root password in .env: DATABASE_ROOT_PASS=correct_password
```

**Error: "DATABASE_URL not set"**
```bash
# Create .env file (copy from .env.example)
# Add your database credentials
```

### API Not Working
```bash
# Make sure backend is running on port 8000
# Check terminal 1 for error messages
```

### Frontend Not Loading
```bash
# Make sure frontend is running on port 5173
# Check terminal 2 for error messages
# Clear browser cache: Ctrl+Shift+Delete
```

---

## 📚 Full Documentation

See [SETUP.md](SETUP.md) for:
- Detailed troubleshooting
- Manual database setup (if needed)
- API endpoint documentation
- Production deployment guide
- Testing with Swagger UI

---

## 🎯 Features Included

✅ **Farmer Management**
- Create, view, update, delete farmers
- Manage multiple plots per farmer

✅ **Agricultural Advisory**
- Get recommendations based on crop symptoms
- Weather impact analysis

✅ **Security**
- API key authentication
- Input validation
- Error handling

✅ **Professional UI**
- Responsive design
- Table views
- Real-time feedback

✅ **Logging & Monitoring**
- Request/response logging
- Error tracking
- Debug information

---

## 💡 Pro Tips

1. **API Documentation** → Visit `http://localhost:8000/docs` after starting backend
2. **Sample Data** → Setup script asks if you want sample farmer data
3. **Environment** → Always use `.env` file for credentials (never commit it!)
4. **Logs** → Check terminal console for detailed operation logs

---

**Need help?** Check [SETUP.md](SETUP.md) for comprehensive guide!

Happy farming! 🌾
