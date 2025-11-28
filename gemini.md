# NearBuy Project Context

## 1. Project Overview
NearBuy is a hyperlocal shop finder application that allows users to discover nearby shops (within a 2-5 meter radius) stocking specific items. It features real-time inventory tracking, accurate spatial queries, and a fast geo-search engine.

## 2. Tech Stack

### Backend
- **Framework:** FastAPI
- **Database:** PostgreSQL with PostGIS (Spatial data)
- **Search Engine:** Typesense (Geo-Search, Typo-tolerance)
- **ORM:** SQLAlchemy (Async), SQLModel
- **Migrations:** Alembic
- **Containerization:** Docker, Docker Compose
- **Authentication:** Cookie-based (Users, Vendors, Contributors)

### Frontend
- **Framework:** Next.js 16 (React 19)
- **Styling:** Tailwind CSS v4
- **Maps:** Leaflet (React Leaflet)
- **Animations:** Framer Motion
- **Icons:** Lucide React
- **Validation:** Zod, React Hook Form

## 3. Architecture

### Backend (`app/`)
- **`api/v1/`**: RESTful API endpoints.
- **`core/`**: Configuration (`config.py`), security, and session management.
- **`db/`**: Database models (`models/`) and session handling (`session.py`).
- **`services/`**: Business logic (e.g., search, inventory).
- **`helpers/`**: Utility functions.
- **`tests/`**: Pytest suite.

### Frontend (`frontend/src/`)
- **`app/`**: Next.js App Router pages (`page.tsx`, `layout.tsx`).
- **`components/`**: Reusable UI components.
    - `Hero.tsx`: Main search section.
    - `ShopCard.tsx`: Display shop details.
    - `Map.tsx`, `MapModal.tsx`: Map visualizations.
- **`lib/`**: Utility libraries.
- **`services/`**: API client services (`api.ts`).
- **`types/`**: TypeScript interfaces.

## 4. Key Features
- **Hyperlocal Search:** Find items in shops near a specific location.
- **Real-time Inventory:** Track stock levels for items in shops.
- **Vendor Management:** Shop owners can manage their shops and inventory.
- **Interactive Maps:** Visual representation of shop locations.
- **Modern UI:** Aesthetic design with animations and responsive layout.

## 5. Setup & Run

### Prerequisites
- Docker & Docker Compose
- Node.js (for local frontend dev)
- Python 3.10+ (for local backend dev)

### Running with Docker
```bash
docker-compose up --build
```

### Local Development
**Backend:**
```bash
cd NearBuy
# Setup venv and install dependencies
pip install -r requirements.txt # or use uv
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 6. Database & Search
- **PostgreSQL:** Stores user, shop, and inventory data. Uses PostGIS for location queries.
- **Typesense:** Indexes shop and item data for fast, typo-tolerant search. Synced with PostgreSQL.

## 7. Current Status
- Backend API is functional with search, auth, and inventory management.
- Frontend is built with Next.js and integrates with the backend.
- Seeding scripts (`scripts/`) are available for populating test data.
