# PropSales AI - FastAPI Backend API

High-performance FastAPI service providing RESTful endpoints and PostgreSQL/Supabase database integrations for PropSales AI Real Estate Management OS.

## 🚀 Features

- **FastAPI Framework**: High performance, auto-generated OpenAPI documentation, and asynchronous endpoints.
- **RESTful Endpoints**:
  - `/api/v1/auth`: Authentication & User Role resolution
  - `/api/v1/projects`: Real Estate Project & Inventory Management
  - `/api/v1/flats`: Unit/Flat details, status updates, pricing, and availability
  - `/api/v1/leads`: Lead ingestion, stage tracking, and executive assignment
  - `/api/v1/site_visits`: Site visit booking & calendar management
  - `/api/v1/team`: Sales Executive directory & performance analytics
  - `/api/v1/payments`: Milestone payment schedules & transaction tracking
  - `/api/v1/analytics`: Executive performance & inventory monetization analytics
  - `/api/v1/ai_chat`: RAG AI Assistant chat integration
- **SQLAlchemy ORM**: Clean database models and session management.
- **Pydantic Schemas**: Strict data validation & typing for request/response bodies.

## 🛠️ Setup & Local Development

### 1. Clone Repository & Navigate to Backend
```bash
git clone https://github.com/13919201819/prop-os-back.git
cd prop-os-back
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your database URL and secret key in `.env`.

### 4. Run Development Server
```bash
uvicorn main:app --reload --port 8000
```
Interactive API documentation will be available at `http://localhost:8000/docs`.

## 📁 Directory Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # API route handlers
│   │       └── api.py         # Main API router
│   ├── core/                  # Security & Config settings
│   ├── db/                    # Database session & base ORM
│   ├── models/                # SQLAlchemy database models
│   └── schemas/               # Pydantic request/response schemas
├── main.py                    # FastAPI application entrypoint
├── requirements.txt           # Python dependencies
└── .env.example               # Sample environment configuration
```
