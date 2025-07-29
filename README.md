# 🧭 Hyperlocal Shop Finder – Backend

A location-based backend service that helps users discover nearby shops (within a 2–5 meter radius) that stock specific items — like “Maggie”, “batteries”, or “coffee sachets” — with real-time availability, quantity, and shop status.

This backend is designed with extensibility, scalability, and modularity in mind — ideal for production-grade deployments as well as developer onboarding.

---

## ✨ Features

- **Geo-based Search API** — find shops within 2–5m that stock an item.
- **Inventory Tracking** — per shop, per item, with real-time quantity updates.
- **PostGIS Spatial Queries** — accurate distance-based shop lookup.
- **Modular API Structure** — RESTful and versioned (`/api/v1`).
- **Cookie-based Auth** — optional login for users, mandatory for shop owners.
- **Clean Architecture** — with layered services, reusable schema, and test coverage.
- **Docker-Ready** — includes dev containers with PostgreSQL + PostGIS.

---

## 🚀 API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/users/signup/user`          | Register a new user. |
| POST   | `/users/signup/vendor`        | Register a new vendor. |
| POST   | `/users/signup/contributor`   | Register a new contributor. |
| POST   | `/users/login`                | Cookie-based login for all user types. |
| POST   | `/users/logout`               | Logout and clear the session. |
| GET    | `/search/shops`               | Search for shops by name. |
| GET    | `/search/items`               | Search for items by name or description. |
| POST   | `/shops/create_shop`          | Create a shop (requires vendor or admin auth). |
| GET    | `/shops/{shop_id}`            | Get shop details. |
| PATCH  | `/shops/update_shop`          | Update shop details (requires vendor or admin auth). |
| DELETE | `/shops/{shop_id}`            | Delete a shop (requires admin auth). |
| POST   | `/items/add_item`             | Add a new item to a shop (requires vendor or admin auth). |
| PATCH  | `/items/update_item`          | Update an item in a shop (requires vendor or admin auth). |
| DELETE | `/items/delete_item`          | Delete an item from a shop (requires vendor or admin auth). |
| POST   | `/inventory/add`              | Add inventory for an item in a shop (requires vendor or admin auth). |
| PATCH  | `/inventory/update`           | Update the inventory of an item in a shop (requires vendor or admin auth). |
| DELETE | `/inventory/{inventory_id}`   | Delete an inventory record (requires vendor or admin auth). |

---

## 🗂️ Project Structure

NEARBUY/
├── app/
│ ├── api/ # All API endpoints (versioned, modular)
│ ├── core/ # Settings, session, and core logic
│ ├── db/ # DB models, schemas, and SQLAlchemy session
│ ├── services/ # Business logic for each domain
│ ├── utils/ # Helper functions (geo, validation)
│ └── tests/ # Unit & integration tests
├── scripts/ # Seeders, spatial test scripts
├── alembic/ # DB migrations
├── docker-compose.yml # Dev stack (FastAPI + PostGIS)
├── Dockerfile
├── .env # App config
└── README.md



---

## ⚙️ Setup & Run (Local Dev)

### 📦 Requirements

- Python 3.10+
- Docker + Docker Compose
- `make` (optional for CLI commands)

### 🔧 Steps

```bash
# Clone and go into backend dir
git clone https://github.com/iamrahulroyy/NearBuy
cd NearBuy

# Spin up the dev environment
docker-compose up --build

# Alembic migrations (first time)
docker-compose exec backend alembic upgrade head

# Seed sample data (optional)
docker-compose exec backend python scripts/seed_data.py


🧪 Testing
docker-compose exec backend pytest

🔮 Roadmap
Add email/password recovery

Admin dashboard for shop owners

Caching layer (Redis) for heavy search traffic

WebSocket or long polling for real-time stock updates

QR-based shop linking for instant scan & find

🤝 Contributing
Pull requests and ideas are welcome! Please keep contributions modular and follow the naming/style conventions already established in the repo.

📜 License
MIT © Rahul Roy

🙏 Acknowledgements
FastAPI

PostgreSQL + PostGIS

SQLAlchemy Models & Alembic

Fellow devs and open-source contributors