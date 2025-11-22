# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Minty is a full-stack application repository with separate frontend and backend components.

**Repository**: https://github.com/johnnynu/minty.git
**License**: MIT
**Author**: Johnny Nguyen

## Current Status

**Phase 1 (Backend) - ✅ COMPLETED**

The backend API is fully implemented with:
- ✅ FastAPI application setup
- ✅ SQLAlchemy models for all database tables
- ✅ Alembic database migrations configured
- ✅ Clerk authentication middleware
- ✅ Complete CRUD endpoints for all resources
- ✅ Pydantic schemas for validation

**Next Steps:**
1. Set up database (Supabase PostgreSQL) and update `.env` with connection string
2. Run database migrations: `alembic upgrade head`
3. Configure Clerk keys in `.env`
4. Test API endpoints
5. Begin Phase 2: Frontend development

## Repository Structure

```
minty/
├── backend/                   # ✅ FastAPI backend (COMPLETE)
│   ├── app/
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── routers/          # API endpoints
│   │   ├── middleware/       # Auth middleware
│   │   ├── config.py         # Settings
│   │   ├── database.py       # DB connection
│   │   └── main.py           # FastAPI app
│   ├── alembic/              # Database migrations
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables
│   └── README.md
├── frontend/                  # ⏳ To be initialized (Phase 2)
└── LICENSE                    # MIT License
```

## Important Notes

- Backend API is production-ready and follows best practices
- All endpoints require Clerk authentication except health checks
- Database migrations are configured with Alembic
- API documentation available at `/docs` when server is running

A full-stack budgeting application implementing envelope budgeting methodology, built with FastAPI, React, and deployed on GCP Cloud Run.

## 🎯 Project Goals

- Demonstrate full-stack development with modern auth (Clerk)
- Implement Python backend with FastAPI + SQLAlchemy
- Deploy containerized services to GCP with CI/CD
- Build responsive React TypeScript frontend
- Practice cloud-native architecture patterns

**Timeline:** 2-3 weeks MVP

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL (Supabase)
- **ORM:** SQLAlchemy 2.0 + Alembic migrations
- **Auth:** Clerk SDK (JWT validation)
- **Validation:** Pydantic v2

### Frontend
- **Framework:** React + TypeScript + Vite
- **Auth UI:** Clerk
- **Styling:** TailwindCSS
- **State:** React Query + Context
- **HTTP:** Axios

### Infrastructure
- **Hosting:** GCP Cloud Run (frontend + backend)
- **Database:** Supabase PostgreSQL
- **CI/CD:** GitHub Actions
- **Containers:** Docker (multi-stage builds)

---

## 📋 Core Features (MVP)

- ✅ **Authentication** - Clerk-based auth with JWT validation
- ✅ **Accounts** - Create/edit/delete accounts (checking, savings, credit cards)
- ✅ **Transactions** - Add/edit/delete transactions with filtering
- ✅ **Categories** - Organize spending with category groups
- ✅ **Budget** - Allocate monthly budgets and track spending
- ✅ **Dashboard** - Net worth, budget overview, recent transactions

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           React + TypeScript                │
│     (Clerk Auth + React Query)              │
└──────────────────┬──────────────────────────┘
                   │ HTTPS + JWT
┌──────────────────▼──────────────────────────┐
│            FastAPI Backend                  │
│   (Auth Middleware + Business Logic)        │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        Supabase PostgreSQL                  │
│  (users, accounts, transactions, budget)    │
└─────────────────────────────────────────────┘
```

---

## 💾 Database Schema

### Core Tables
- **users** - `id`, `clerk_user_id`, `email`, `created_at`
- **accounts** - `id`, `user_id`, `name`, `type`, `balance`
- **transactions** - `id`, `user_id`, `account_id`, `category_id`, `date`, `payee`, `amount`, `memo`, `cleared`
- **category_groups** - `id`, `user_id`, `name`, `sort_order`
- **categories** - `id`, `user_id`, `category_group_id`, `name`, `sort_order`
- **budget_allocations** - `id`, `user_id`, `category_id`, `month`, `amount`

### Key Indexes
- `idx_users_clerk_id` on `users(clerk_user_id)`
- `idx_transactions_user_id`, `idx_transactions_date`
- `idx_budget_allocations_user_category` on `budget_allocations(user_id, category_id, month)`

---

## 📈 Development Roadmap

### Phase 1: Backend ✅ COMPLETED
- [x] Database schema and migrations
- [x] Clerk auth integration
- [x] Accounts CRUD endpoints
- [x] Transactions CRUD endpoints
- [x] Categories and budget endpoints
- [x] All Pydantic schemas for validation
- [x] Authentication middleware

### Phase 2: Frontend (Week 2)
- [x] Clerk authentication UI
- [x] Account management interface
- [x] Transaction list and forms
- [x] Budget allocation interface
- [x] Dashboard with summaries

### Phase 3: Deployment (Week 3)
- [x] Docker containerization
- [x] GCP Cloud Run deployment
- [x] GitHub Actions CI/CD
- [x] Documentation and polish

---

## 🎓 Learning Outcomes

This project demonstrates:
- Full-stack TypeScript/Python development
- RESTful API design with FastAPI
- JWT authentication implementation
- PostgreSQL database design
- Docker containerization
- Cloud-native deployment (GCP)
- CI/CD pipeline with GitHub Actions
- Financial application precision handling
- React state management with React Query

---