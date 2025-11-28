# 🧭 NearBuy – Hyperlocal Shop Finder

NearBuy is a location-based application that helps users discover nearby shops (within a 2–5 meter radius) that stock specific items — like “Maggie”, “batteries”, or “coffee sachets” — with real-time availability, quantity, and shop status.

The project consists of a robust **FastAPI backend** and a modern **Next.js frontend**.

---

## ✨ Features

- **⚡ Fast Geo-Search:** Powered by Typesense, find shops within a given radius that stock a specific item.
- **🛒 Real-Time Inventory:** Track stock levels per shop, per item.
- **📍 Accurate Spatial Queries:** Uses PostGIS for precise location data management.
- **🗺️ Interactive Maps:** Visualize shop locations and search results on a map.
- **🔐 Role-Based Auth:** Secure cookie-based authentication for Users, Vendors, and Contributors.
- **📱 Modern UI:** Responsive design built with Next.js, Tailwind CSS, and Framer Motion.
- **🐳 Fully Containerized:** Docker support for consistent development and deployment.

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI
- **Database:** PostgreSQL + PostGIS
- **Search:** Typesense
- **ORM:** SQLAlchemy (Async) + SQLModel
- **Migrations:** Alembic

### Frontend
- **Framework:** Next.js 16 (App Router)
- **Styling:** Tailwind CSS v4
- **Maps:** Leaflet (React Leaflet)
- **State/Validation:** React Hook Form, Zod

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend)
- Python 3.10+ (for local backend)

### 🐳 Run with Docker (Recommended)

The easiest way to run the full stack (Backend + DB + Search) is via Docker.

```bash
# Clone the repository
git clone https://github.com/iamrahulroyy/NearBuy
cd NearBuy

# Start the services
docker-compose up --build
```

### 💻 Local Development

#### Backend
```bash
cd NearBuy
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

#### Frontend
```bash
cd frontend
# Install dependencies
npm install

# Run the development server
npm run dev
```

---

## 🗂️ Project Structure

```
NEARBUY/
├── app/                 # Backend Source Code
│   ├── api/             # API Endpoints
│   ├── core/            # Config & Security
│   ├── db/              # Database Models
│   └── services/        # Business Logic
├── frontend/            # Frontend Source Code
│   ├── src/app/         # Next.js Pages
│   └── src/components/  # UI Components
├── scripts/             # Seeding & Utility Scripts
├── alembic/             # Database Migrations
├── docker-compose.yml   # Docker Services Config
└── README.md            # Project Documentation
```

---

## 🤝 Contributing
Pull requests are welcome! Please ensure your code follows the project's style guidelines.

## 📜 License
MIT © Rahul Roy
