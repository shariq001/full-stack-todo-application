<!-- SYNC IMPACT REPORT -->
<!-- Version change: 1.0.0 → 2.0.0 -->
<!-- Modified principles: Console App → Full-Stack Web App -->
<!-- Added sections: Agentic Workflow, User Isolation, Stateless Architecture, Persistence -->
<!-- Removed sections: In-Memory Persistence, CLI-First Interface -->
<!-- Templates requiring updates: ⚠️ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md -->
<!-- Follow-up TODOs: None -->

# Agentic Full-Stack Todo Web Application Constitution

## Core Principles

### Agentic Workflow (Mandatory)
Adherence to the "Spec → Plan → Task → Implement" cycle via Claude Code (No manual coding); All development must follow the Spec-Driven Development methodology; Ensure every implementation step is traced back to approved tasks and plans.

### User Isolation (NON-NEGOTIABLE)
Strict data privacy where users only access their own records; Implement proper authentication and authorization to enforce user boundaries; Prevent cross-user data access or manipulation; All API endpoints must validate user ownership of requested resources.

### Stateless Architecture
Decoupled frontend and backend using JWT-based authentication; No server-side session storage; Ensure scalability through stateless API design; Maintain clean separation of concerns between client and server responsibilities.

### Persistence (Reliable Storage)
Reliable data storage using Serverless PostgreSQL; Implement proper data integrity constraints and validation; Ensure data durability and consistency across application states; Follow ACID properties for critical operations.

### Clean Architecture
Maintain clear separation between data models, business logic, and user interfaces; Follow established clean architecture patterns with well-defined layers; Ensure each component has a single responsibility and is independently testable.

### Reliability (NON-NEGOTIABLE)
Implement robust error handling for all user inputs and API requests; Validate all user input and authorization tokens before processing; Ensure graceful degradation and informative error messages; Handle network failures and timeouts appropriately.

### Maintainability
Adhere to Clean Code principles with modular, well-documented design; Follow PEP 8 coding standards and Next.js/TypeScript best practices; Write self-documenting code with clear variable names and logical structure; Maintain consistent code style across frontend and backend.

## Technology Standards
Tech Stack: Next.js 16+ (App Router), Python FastAPI, SQLModel, Neon Serverless PostgreSQL, Better Auth; Authentication: JWT implementation with shared secret verification (`BETTER_AUTH_SECRET`) between Next.js and FastAPI; API Design: RESTful endpoints requiring Bearer tokens in Authorization headers; Data Integrity: SQLModel for strict schema enforcement and type safety; Frontend: Responsive interface with persistent state management.

## Development Workflow
Follow Spec-Driven Development with clear spec, plan, and tasks artifacts; Implement using TDD approach where applicable; Ensure all changes are testable and verifiable; Maintain clean commit history with descriptive messages; All implementations must use the specified skills: auth-system, frontend-ui-development, database-management, backend-api-logic.

## Governance

All implementations must comply with these constitutional principles; Changes to this constitution require explicit approval and documentation; Each principle is testable and verifiable through code review and automated checks; Deviations from these principles must be justified and documented; Database must use Neon Serverless PostgreSQL and Auth Provider must be Better Auth with JWT plugin.

**Version**: 2.0.0 | **Ratified**: 2026-01-10 | **Last Amended**: 2026-02-02
