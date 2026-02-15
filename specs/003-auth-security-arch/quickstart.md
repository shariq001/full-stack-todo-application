# Quickstart Guide: Authentication & Security Architecture

**Feature**: Authentication & Security Architecture
**Date**: 2026-02-04
**Version**: 1.0

## Overview

This guide provides step-by-step instructions to set up the authentication and security architecture using Better Auth for JWT token issuance and FastAPI for stateless token verification with a shared secret.

## Prerequisites

- Node.js 18+ and npm/yarn for frontend
- Python 3.10+ with pip for backend
- Git for version control
- A secure shared secret for JWT signing

## Environment Setup

### 1. Create Environment Variables

**Frontend (Next.js):**
```bash
# frontend/.env.local
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
```

**Backend (FastAPI):**
```bash
# backend/.env
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
```

⚠️ **Security Note**: Use different secrets for development and production environments.

### 2. Install Dependencies

**Frontend Dependencies:**
```bash
cd frontend
npm install better-auth @better-auth/react
# or
yarn add better-auth @better-auth/react
```

**Backend Dependencies:**
```bash
cd backend
pip install fastapi python-jose[cryptography] python-multipart python-dotenv
```

## Frontend Setup (Better Auth)

### 1. Configure Better Auth

Create `frontend/pages/api/auth/[...nextauth].ts`:

```typescript
import { init } from "better-auth";
import { nextJs } from "@better-auth/next-js";

export const {
  getServerSession,
  signOut,
  signUp,
  signIn,
  verifyEmail,
  forgotPassword,
  resetPassword,
  updatePassword,
  changeEmail,
  verifyAuth,
} = init({
  secret: process.env.BETTER_AUTH_SECRET!,
  trustHost: true,
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    // Configure social login providers if needed
  },
  jwt: {
    expiresIn: "15m", // Token expiration
  },
});

export { nextJs };
export default nextJs.adapter(nextOptions);
```

### 2. Initialize Auth Context

Create `frontend/src/auth/auth-context.ts`:

```typescript
import { createContext, useContext } from "react";
import { Session } from "better-auth";

interface AuthContextType {
  session: Session | null;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType>({
  session: null,
  isLoading: true,
});

export const useAuth = () => useContext(AuthContext);
```

## Backend Setup (FastAPI JWT Verification)

### 1. Create JWT Utilities

Create `backend/src/auth/jwt.py`:

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from pydantic import BaseModel
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify JWT token using shared secret and return user data
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None or email is None:
            return None

        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except JWTError:
        return None

def is_token_expired(token: str) -> bool:
    """
    Check if JWT token is expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload.get("exp")

        if exp_timestamp is None:
            return True

        current_time = datetime.utcnow().timestamp()
        return current_time > exp_timestamp
    except JWTError:
        return True
```

### 2. Create FastAPI Dependencies

Create `backend/src/auth/dependencies.py`:

```python
from fastapi import Depends, HTTPException, status, Request
from .jwt import verify_token, is_token_expired, TokenData

async def get_current_user(request: Request) -> TokenData:
    """
    FastAPI dependency to extract and verify JWT from Authorization header
    """
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ")[1]  # Extract token after "Bearer "

    if is_token_expired(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = verify_token(token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data
```

## Protected Routes Example

### 1. Using the Dependency

Create or update `backend/src/api/example_protected_route.py`:

```python
from fastapi import APIRouter, Depends
from ..auth.dependencies import get_current_user
from ..auth.jwt import TokenData

router = APIRouter()

@router.get("/protected-data")
async def get_protected_data(current_user: TokenData = Depends(get_current_user)):
    """
    Example of a protected route that requires authentication
    """
    return {
        "message": f"Hello {current_user.email}",
        "user_id": current_user.user_id,
        "access_granted": True
    }
```

## Testing the Authentication

### 1. Start the Backend Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test with Valid Token

```bash
curl -X GET http://localhost:8000/protected-data \
  -H "Authorization: Bearer your-valid-jwt-token-here"
```

### 3. Test with Invalid Token

```bash
curl -X GET http://localhost:8000/protected-data \
  -H "Authorization: Bearer invalid-token-here"
```

Expected response: `401 Unauthorized`

### 4. Test Without Token

```bash
curl -X GET http://localhost:8000/protected-data
```

Expected response: `401 Unauthorized`

## Verification Commands

### 1. Verify Environment Variables

```bash
# In backend directory
python -c "import os; print('Secret configured:', bool(os.getenv('BETTER_AUTH_SECRET')))"
```

### 2. Test JWT Verification Functionality

Create a test script `backend/test_auth.py`:

```python
import sys
sys.path.append('.')

from src.auth.jwt import verify_token

# Test token verification with a sample token
# Note: You'll need a real token from Better Auth for actual testing
print("JWT verification module loaded successfully")
```

## Key Components

### Frontend Components
- `frontend/src/auth/better-auth.ts` - Better Auth configuration
- `frontend/src/auth/auth-context.ts` - Authentication context provider

### Backend Components
- `backend/src/auth/jwt.py` - JWT encoding/decoding utilities
- `backend/src/auth/dependencies.py` - FastAPI authentication dependencies
- `backend/src/api/deps.py` - Global dependencies

## Troubleshooting

### Common Issues

1. **Token Verification Fails**:
   - Verify `BETTER_AUTH_SECRET` is identical in frontend and backend
   - Check that the token format is correct (Bearer <token>)
   - Ensure the token hasn't expired

2. **Environment Variables Not Loading**:
   - Confirm .env files exist in correct locations
   - Verify python-dotenv is properly installed
   - Check file permissions on .env files

3. **401 Unauthorized Errors**:
   - Verify Authorization header format
   - Check that token is properly formatted JWT
   - Ensure token hasn't expired

### Verification Commands

```bash
# Test backend JWT dependency
curl -v -X GET http://localhost:8000/health
# Should return 200 OK if auth is configured correctly

# Test protected endpoint with valid token
curl -v -X GET http://localhost:8000/protected-data \
  -H "Authorization: Bearer your-jwt-token"
```

## Next Steps

1. Implement frontend authentication UI components
2. Create more protected API endpoints using the `get_current_user` dependency
3. Add role-based authorization (RBAC) for advanced permissions
4. Implement token refresh functionality for improved user experience
5. Add comprehensive error handling and logging

## Security Notes

- Always use HTTPS in production
- Store secrets securely using environment variables
- Rotate secrets regularly
- Monitor authentication failures for potential attacks
- Implement rate limiting for authentication endpoints