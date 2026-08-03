## Notes
- v1 is intentionally simple — a browser UI, a backend API, one database.
- Future additions (not in v1):
  - Authentication service (JWT-based)
  - Validation/quality-check worker (runs on a schedule)
  - Reporting/export service
  - Caching layer for fast search (if needed later)# High-Level Architecture

Users
  ↓
Frontend
  ↓
Backend
  ↓
PostgreSQL Database

