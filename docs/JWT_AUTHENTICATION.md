# JWT Authentication Implementation Guide

This document outlines the complete JWT (JSON Web Token) authentication system implemented for the Agri Advisory application, replacing the previous hardcoded API key system.

## Overview

The application now uses a secure, user-based authentication system with:
- User registration and login
- Password hashing with bcrypt
- JWT tokens (access + refresh pattern)
- Protected endpoints requiring valid Bearer tokens
- Automatic token refresh on expiration

## Backend Implementation

### 1. Authentication Module ([backend/app/auth.py](../backend/app/auth.py))

Core JWT and password utilities:

**Functions:**
- `hash_password(password)` - Bcrypt password hashing
- `verify_password(plain_password, hashed_password)` - Password validation
- `create_access_token(data)` - Generate 30-minute JWT access token
- `create_refresh_token(data)` - Generate 7-day JWT refresh token
- `verify_token(token)` - Decode and validate JWT signature
- `get_current_user_id()` - FastAPI dependency for extracting user ID from Bearer token

**Configuration:**
- Algorithm: HS256 (HMAC with SHA-256)
- Access Token Expiration: 30 minutes
- Refresh Token Expiration: 7 days
- Secret Key: Retrieved from `SECRET_KEY` environment variable

### 2. Authentication Endpoints ([backend/app/routers/auth.py](../backend/app/routers/auth.py))

All endpoints require JSON request body and return standardized responses:

#### POST `/api/auth/register`
Create a new user account.

**Request:**
```json
{
  "username": "farmer_name",
  "email": "farmer@example.com",
  "password": "secure_password"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "farmer_name",
    "email": "farmer@example.com"
  }
}
```

**Validation Rules:**
- Username: 3-50 characters, must be unique
- Email: Valid email format, must be unique (lowercase stored)
- Password: 6-100 characters

**Error Responses:**
- 422: Validation error (username/email exists, invalid format)
- 500: Server error

#### POST `/api/auth/login`
Authenticate with credentials.

**Request:**
```json
{
  "username": "farmer_name",
  "password": "secure_password"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "farmer_name",
    "email": "farmer@example.com"
  }
}
```

**Error Responses:**
- 401: Invalid credentials
- 422: Validation error

#### POST `/api/auth/refresh`
Get a new access token using the refresh token.

**Request Header:**
```
Authorization: Bearer <refresh_token>
```

**Response (200):**
```json
{
  "access_token": "new_eyJhbGc...",
  "refresh_token": "new_eyJhbGc...",
  "token_type": "bearer",
  "user": { ... }
}
```

**Error Responses:**
- 401: Invalid or expired refresh token

#### GET `/api/auth/me`
Get current authenticated user details.

**Request Header:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "username": "farmer_name",
  "email": "farmer@example.com"
}
```

**Error Responses:**
- 401: Missing or invalid token

#### POST `/api/auth/logout`
Logout user (client-side token removal).

**Request Header:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

### 3. User Model ([backend/app/models.py](../backend/app/models.py))

**Database Table: User**
- `id`: Integer primary key (auto-increment)
- `username`: String(50), unique, indexed
- `email`: String(100), unique, indexed, lowercase
- `password_hash`: String (bcrypt hash)
- `created_at`: DateTime (ISO format)

**Additional Models:**
- `UserValidation`: Base validation model with field validators
- `UserCreate`: Registration request model
- `UserLogin`: Login credentials model
- `UserResponse`: Safe user response (no password_hash)
- `Token`: Authentication response with tokens

### 4. Protected Endpoints

All endpoints now require JWT authentication:

**Farmer Endpoints:**
- GET `/api/farmers/`
- POST `/api/farmers/`
- GET `/api/farmers/{farmer_id}`
- PUT `/api/farmers/{farmer_id}`
- DELETE `/api/farmers/{farmer_id}`
- POST `/api/farmers/{farmer_id}/plots`
- GET `/api/farmers/{farmer_id}/plots`
- DELETE `/api/farmers/{farmer_id}/plots/{plot_id}`

**Advisory Endpoints:**
- POST `/api/advisory/recommend`

**Usage:**
All requests must include the authorization header:
```
Authorization: Bearer <access_token>
```

Responses:
- 401: Missing or invalid token
- 403: Insufficient permissions
- 200: Success

## Frontend Implementation

### 1. Authentication Context ([frontend/src/context/AuthContext.jsx](../frontend/src/context/AuthContext.jsx))

Global state management for authentication using React Context API.

**Provides:**
- `user`: Current authenticated user object
- `accessToken`: JWT access token
- `refreshToken`: JWT refresh token
- `loading`: Loading state during auth operations
- `error`: Error message from last operation
- `isAuthenticated`: Boolean authentication status

**Functions:**
- `login(username, password)`: Authenticate user
- `register(username, email, password)`: Create new account
- `logout()`: Clear auth state and tokens

**Features:**
- Automatic token refresh on 401 response
- Token persistence in localStorage
- Axios interceptor for automatic token injection in requests
- Auto-login from stored tokens on app startup

### 2. Login Page ([frontend/src/pages/LoginPage.jsx](../frontend/src/pages/LoginPage.jsx))

User-friendly login/registration UI.

**Features:**
- Toggle between login and register modes
- Form validation
- Error message display
- Loading states
- Callback on successful authentication

**Styling:**
- Responsive design with gradient background
- Clean form layout
- User-friendly error messages

### 3. Protected Routes ([frontend/src/components/ProtectedRoute.jsx](../frontend/src/components/ProtectedRoute.jsx))

Route wrapper component to enforce authentication.

**Features:**
- Checks authentication status
- Shows loading state while checking
- Prevents access to protected pages without token

### 4. Updated Components

All components now use JWT tokens instead of API key:

**FarmerForm.jsx**
- Uses `useAuth()` hook to get access token
- Sends token in Authorization header

**FarmerList.jsx**
- Fetches farmer list with JWT
- Updates/deletes farmers with JWT
- Displays user-specific data

**PlotForm.jsx**
- Adds plots per authenticated user
- Uses JWT for authorization

**AdvisoryPanel.jsx**
- Gets recommendations with JWT
- User-specific advisory tracking

### 5. Main App Component ([frontend/src/App.jsx](../frontend/src/App.jsx))

Enhanced with:
- AuthProvider wrapper for context
- Conditional rendering based on authentication
- User greeting in header
- Logout button
- Loading state handling

## Environment Configuration

Required environment variables in `.env`:

```env
# Database
DATABASE_URL=mysql+pymysql://agriuser:harshal@localhost:3306/agri?charset=utf8mb4

# JWT Secret (IMPORTANT: Change in production!)
SECRET_KEY=your-secret-key-change-in-production-please-use-a-long-random-string

# App Settings
APP_HOST=0.0.0.0
APP_PORT=8000

# Frontend
FRONTEND_URL=http://localhost:5173
```

## Dependencies

**Backend (added):**
- `python-jose[cryptography]>=3.3.0` - JWT generation and validation
- `passlib[bcrypt]>=1.7.4` - Password hashing

**Frontend:**
- `axios` - HTTP client (already present)
- React Context API - State management (built-in)

## Workflow

### 1. User Registration
1. New user fills registration form
2. Client sends POST to `/api/auth/register`
3. Backend creates User with hashed password
4. Backend returns access and refresh tokens
5. Client stores tokens in localStorage
6. AuthContext automatically logs user in
7. App redirects to dashboard

### 2. User Login
1. Existing user fills login form
2. Client sends POST to `/api/auth/login`
3. Backend validates credentials
4. Backend returns tokens
5. Same as registration steps 4-7

### 3. Protected Requests
1. Component calls API with data
2. Axios interceptor automatically adds token to header
3. Backend validates token and extracts user_id
4. Request processed for that user
5. If token expired, interceptor refreshes token
6. Request automatically retried with new token

### 4. Logout
1. User clicks logout button
2. Client clears localStorage
3. AuthContext updates state
4. App redirects to login page

## Security Considerations

### Current Implementation
✅ Passwords hashed with bcrypt (salted, slow)
✅ Tokens signed with HMAC-SHA256
✅ Access tokens have short expiration (30 min)
✅ Refresh tokens stored separately
✅ User IDs embedded in tokens (no sensitive data)
✅ CORS configured for frontend domain

### Production Recommendations
- ⚠️ Change `SECRET_KEY` to a long random string
- ⚠️ Update `FRONTEND_URL` to production domain
- ⚠️ Enable HTTPS for all communication
- ⚠️ Implement refresh token rotation
- ⚠️ Add rate limiting on auth endpoints
- ⚠️ Implement logout token blacklist
- ⚠️ Add request signing for integrity
- ⚠️ Store refresh tokens in httpOnly cookies
- ⚠️ CSRF protection for POST requests

## Testing

### Manual Testing with Postman

**1. Register New User**
```
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
  "username": "testfarmer",
  "email": "test@example.com",
  "password": "Test@1234"
}
```

**2. Login**
```
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "username": "testfarmer",
  "password": "Test@1234"
}
```
Save the `access_token` from response.

**3. Access Protected Endpoint**
```
GET http://localhost:8000/api/farmers/
Authorization: Bearer <access_token_from_above>
```

**4. Refresh Token**
```
POST http://localhost:8000/api/auth/refresh
Authorization: Bearer <refresh_token_from_login_response>
```

**5. Get Current User**
```
GET http://localhost:8000/api/auth/me
Authorization: Bearer <access_token>
```

## Troubleshooting

### "401 Unauthorized"
- Ensure token is included in Authorization header
- Verify token hasn't expired
- Check token is from `/api/auth/login` not `/api/auth/refresh`

### "Token is invalid"
- Confirm `SECRET_KEY` is set in `.env`
- Ensure token wasn't modified
- Check backend and frontend have same SECRET_KEY

### "User not found"
- Verify user exists (register first)
- Check username/password spelling
- Database must have User table

### Token doesn't auto-refresh
- Refresh token must be stored in localStorage
- Check browser console for CORS errors
- Verify frontend FRONTEND_URL matches cors_allow_origins

### Can't login from frontend
- Ensure backend is running on port 8000
- Check database credentials in DATABASE_URL
- Run `python init_db.py` to initialize User table
- Check browser network tab for 422/500 errors

## File Structure

```
backend/
├── app/
│   ├── auth.py              # JWT utilities
│   ├── models.py            # Updated with User model
│   ├── main.py              # Updated with auth router
│   ├── db.py                # Database setup
│   └── routers/
│       ├── auth.py          # Authentication endpoints
│       ├── farmers.py       # Updated for JWT
│       └── advisory.py      # Updated for JWT
├── requirements.txt         # Updated with jwt/bcrypt packages
└── ...

frontend/
├── src/
│   ├── App.jsx              # Updated with auth
│   ├── main.jsx             # Entry point
│   ├── styles.css           # Updated styles
│   ├── context/
│   │   └── AuthContext.jsx  # Auth state management
│   ├── pages/
│   │   └── LoginPage.jsx    # Login/register UI
│   └── components/
│       ├── FarmerForm.jsx   # Updated for JWT
│       ├── FarmerList.jsx   # Updated for JWT
│       ├── PlotForm.jsx     # Updated for JWT
│       ├── AdvisoryPanel.jsx # Updated for JWT
│       └── ProtectedRoute.jsx # Route protection
└── ...

.env                        # Updated with SECRET_KEY
```

## Next Steps

1. **Database Migration**: The User table will be auto-created when you run the backend
   ```bash
   python backend/app/main.py
   ```

2. **Test the System**:
   - Start backend: `python backend/app/main.py`
   - Start frontend: `npm run dev` (from frontend folder)
   - Try registering in the login page
   - Verify farmer operations work with JWT

3. **Production Hardening**:
   - Update SECRET_KEY with strong random string
   - Enable HTTPS
   - Configure CORS for production domain
   - Implement token blacklist for logout
   - Set up token rotation

## Migration from API Key

The system automatically:
- ✅ Removed hardcoded API_KEY from all components
- ✅ Updated all API calls to use JWT tokens
- ✅ Wrapped app with AuthProvider
- ✅ Added login/logout functionality
- ✅ Implemented token auto-refresh

**Old code (removed):**
```javascript
const API_KEY = "default-dev-key";
headers: { "x-api-key": API_KEY }
```

**New code (in use):**
```javascript
const { accessToken } = useAuth();
headers: { Authorization: `Bearer ${accessToken}` }
```

## Support

For issues or questions:
1. Check error messages in browser console
2. Review backend logs for detailed errors
3. Verify all environment variables are set
4. Ensure database is running
5. Check that both frontend and backend are started
