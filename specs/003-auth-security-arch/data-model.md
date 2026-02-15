# Data Model: Authentication & Security Architecture

**Feature**: Authentication & Security Architecture
**Date**: 2026-02-04
**Data Model Version**: 1.0

## Authentication Entity Definitions

### JWT Token
- **Structure**: Compact, URL-safe token with three parts (header, payload, signature)
- **Purpose**: Carry authentication and authorization information between frontend and backend

#### JWT Header Fields:
- `alg`: Algorithm used for signing
  - Value: "HS256" (HMAC SHA-256)
  - Type: String
  - Required: Yes

- `typ`: Token type
  - Value: "JWT"
  - Type: String
  - Required: Yes

#### JWT Payload Claims:
- `sub`: Subject (User ID)
  - Type: String
  - Required: Yes
  - Description: Unique identifier for the authenticated user

- `email`: User Email
  - Type: String
  - Required: Yes
  - Description: Email address of the authenticated user

- `iat`: Issued At
  - Type: NumericDate
  - Required: Yes
  - Description: Unix timestamp of token creation

- `exp`: Expiration Time
  - Type: NumericDate
  - Required: Yes
  - Description: Unix timestamp of token expiration

- `jti`: JWT ID (optional)
  - Type: String
  - Required: No
  - Description: Unique identifier for the token

### Authentication Configuration
- **Entity**: Auth Configuration
- **Purpose**: Store authentication settings and secrets

#### Configuration Fields:
- `BETTER_AUTH_SECRET`: Shared authentication secret
  - Type: String
  - Required: Yes
  - Security: Should be stored securely as environment variable
  - Description: Secret key used to sign and verify JWT tokens

- `JWT_ALGORITHM`: Signing algorithm
  - Type: String
  - Required: Yes
  - Default: "HS256"
  - Description: Algorithm used for signing JWT tokens

- `TOKEN_EXPIRATION_MINUTES`: Access token duration
  - Type: Integer
  - Required: Yes
  - Default: 15
  - Description: Duration in minutes before access token expires

## Security Context Objects

### Current User Object
- **Purpose**: Representation of authenticated user context available in backend handlers

#### User Object Fields:
- `id`: User identifier
  - Type: String
  - Required: Yes
  - Description: Unique identifier extracted from JWT token

- `email`: User email
  - Type: String
  - Required: Yes
  - Description: Email address extracted from JWT token

- `authenticated`: Authentication status
  - Type: Boolean
  - Required: Yes
  - Default: True
  - Description: Flag indicating successful authentication

### Authentication Headers
- **Purpose**: HTTP header structure for carrying authentication tokens

#### Header Structure:
- `Authorization`: Authentication header
  - Format: "Bearer {token}"
  - Required: Yes for protected endpoints
  - Example: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

## API Contract Specifications

### Authenticated Endpoint Requirements
- All protected endpoints must include Authorization header
- Token must be in Bearer format
- Token must be valid and not expired
- Token signature must match shared secret

### Error Response Models
- **401 Unauthorized Response**:
  - Structure: `{ "detail": "Authentication required" }`
  - Trigger: Missing, invalid, or expired token
  - Message: Generic to avoid revealing specific security details

- **403 Forbidden Response**:
  - Structure: `{ "detail": "Insufficient permissions" }`
  - Trigger: Valid token but insufficient privileges (future use)
  - Message: Generic to avoid revealing specific security details

## Session State Management (Frontend)

### Session Data Structure
- `user`: User information object
  - Contains: id, email, name (from Better Auth)
  - Purpose: Cached user data for UI display

- `accessToken`: JWT token string
  - Purpose: Token for authenticating backend API requests
  - Storage: Browser storage (secure configuration)

- `expiresAt`: Token expiration timestamp
  - Type: Date/Unix timestamp
  - Purpose: Track token validity for proactive refresh

## Backend Authentication Flow

### Request Processing Chain
1. FastAPI receives request with Authorization header
2. `get_current_user` dependency extracts token
3. Token signature is verified using shared secret
4. Token expiration is validated
5. User claims are extracted into Current User object
6. Request is processed with authenticated user context

## Security Constraints

### Token Validation Rules
- Must have valid JWT format (3 parts separated by dots)
- Signature must match shared secret using HS256
- Current time must be before expiration time
- All required claims must be present

### Secret Management Constraints
- `BETTER_AUTH_SECRET` must be at least 32 characters
- Secret must be identical across frontend and backend
- Secret must not be hardcoded in source code
- Secret must be stored in environment variables

### Expiration Policies
- Access tokens expire after TOKEN_EXPIRATION_MINUTES
- Token expiration check must occur before processing protected endpoints
- Client-side should implement token refresh before expiration