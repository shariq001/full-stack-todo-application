# Implementation Plan: Authentication & Security Architecture

**Branch**: `003-auth-security-arch` | **Date**: 2026-02-04 | **Spec**: [specs/003-auth-security-arch/spec.md](specs/003-auth-security-arch/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of authentication and security architecture using Better Auth for JWT token issuance on the frontend and stateless JWT verification middleware on the backend using a shared secret. The architecture ensures secure, stateless communication between frontend and backend with proper error handling for invalid/expired tokens.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: TypeScript (Next.js 16+), Python 3.10+
**Primary Dependencies**: Better Auth, Next.js, FastAPI, PyJWT, python-jose
**Storage**: N/A (stateless authentication)
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application (Cross-platform)
**Project Type**: Web application (Frontend + Backend)
**Performance Goals**: <100ms token verification, maintain stateless operation
**Constraints**: <200ms p95 authentication response time, no database session checks
**Scale/Scope**: Support initial 10k users with horizontal scaling capability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Agentic Workflow: Follow "Spec → Plan → Task → Implement" cycle as per constitution
- User Isolation: Ensure JWT verification includes proper user identification
- Stateless Architecture: Maintain stateless JWT verification without server-side sessions
- Persistence: N/A for authentication layer (tokens are stateless)
- Clean Architecture: Clear separation between auth logic and business logic
- Reliability: Proper error handling for authentication failures
- Maintainability: Follow best practices for security implementations

## Architecture Flow Diagram

### Token Issuance Flow
```
User Login Action
        ↓
   Better Auth
        ↓
   JWT Token Created
   (signed with shared secret)
        ↓
   Token Stored Client-Side
   (Browser Storage/Cookie)
```

### API Request Flow
```
Client Request with Authorization Header
        ↓
   FastAPI Dependency: get_current_user
        ↓
   JWT Token Extraction from Bearer Header
        ↓
   Token Verification using Shared Secret
        ↓
   User Info (ID, Email) Extracted
        ↓
   Request Processed with User Context
```

### Security Middleware Flow
```
HTTP Request → Extract Token → Verify Signature → Decode Claims → Validate Expiration → Extract User → Process Request
                ↓              ↓                  ↓               ↓                    ↓               ↓
           Bearer Header   HS256 Match    Shared Secret    Token Valid    Within Expiry   Attach User Context
```

## Project Structure

### Documentation (this feature)

```text
specs/003-auth-security-arch/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command output)
├── data-model.md        # Phase 1 output (/sp.plan command output)
├── quickstart.md        # Phase 1 output (/sp.plan command output)
├── contracts/           # Phase 1 output (/sp.plan command output)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── auth/
│   │   ├── better-auth.ts    # Better Auth configuration
│   │   ├── auth-context.ts   # Authentication context
│   │   └── auth-utils.ts     # Authentication utility functions
│   ├── components/
│   │   └── auth/             # Authentication components (to be built later)
│   └── types/
│       └── auth.ts           # Authentication type definitions
├── pages/
│   ├── api/
│   │   └── auth/
│   │       └── [...nextauth].ts  # Better Auth API routes
├── .env.local              # Local environment variables (gitignored)
└── .env.example            # Example environment variables

backend/
├── src/
│   ├── auth/
│   │   ├── jwt.py          # JWT encoding/decoding utilities
│   │   ├── dependencies.py # FastAPI dependencies (get_current_user)
│   │   ├── utils.py        # Authentication utility functions
│   │   └── schemas.py      # Authentication-related schemas
│   ├── config/
│   │   └── settings.py     # Configuration including auth settings
│   ├── api/
│   │   └── deps.py         # Global dependencies including auth
│   └── main.py             # Application entry point
├── requirements.txt
├── .env                    # Environment variables (gitignored)
└── .env.example            # Example environment variables

tests/
├── auth/
│   ├── test_jwt.py         # JWT utility tests
│   ├── test_auth_deps.py   # Authentication dependency tests
│   └── test_better_auth.py # Better Auth integration tests
└── conftest.py             # Pytest configuration
```

**Structure Decision**: Web application with separate frontend and backend directories to maintain clear separation of concerns. Frontend handles Better Auth integration while backend manages JWT verification through reusable FastAPI dependencies.

## Key Design Decisions

1. **Token Expiration Policy**:
   - Access tokens: 15 minutes expiry
   - Refresh tokens: 7 days expiry (managed by Better Auth)
   - Refresh rotation: Enabled to prevent refresh token theft

2. **Error Handling Strategy**:
   - 401 Unauthorized: Invalid/missing token
   - 403 Forbidden: Valid token but insufficient permissions (future use)

3. **Phased Implementation Strategy**:
   - Phase 1: Frontend Auth Setup → Configure Better Auth in Next.js for session creation
   - Phase 2: Shared Secret Config → Ensure `BETTER_AUTH_SECRET` matches across services
   - Phase 3: Backend Middleware → Create reusable FastAPI dependency `get_current_user`
   - Phase 4: Verification Testing → Test protected routes with valid vs. invalid tokens

4. **Security Best Practices**:
   - Tokens signed with strong HS256 algorithm
   - Secure storage of `BETTER_AUTH_SECRET`
   - Proper token validation including expiration checks
   - Stateless verification without database lookups

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |