# 🧭 Hyperlocal Shop Finder – Backend

A location-based backend service that helps users discover nearby shops (within a 2–5 meter radius) that stock specific items — like “Maggie”, “batteries”, or “coffee sachets” — with real-time availability, quantity, and shop status.

This backend is designed with extensibility, scalability, and modularity in mind, and is powered by FastAPI, PostgreSQL with PostGIS, and Typesense for lightning-fast, typo-tolerant geo-search.



---
✨ Features

⚡ Fast Geo-Search API: Powered by Typesense, find shops within a given radius that stock a specific item.

🛒 Real-Time Inventory Tracking: Per shop, per item, with real-time quantity updates.

📍 Accurate Spatial Queries: Uses PostGIS for storing and managing location data.

🧾 Modular API Structure: RESTful and versioned (/api/v1) for clean separation of concerns.

🔐 Cookie-based Authentication: Secure, optional login for users and mandatory authentication for shop owners.

🐳 Fully Containerized: The entire stack, including the database and search engine, is managed with Docker for a consistent development environment.

---

## 🚀 API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/users/signup/user`          | Register a new user. |
| POST   | `/users/signup/vendor`        | Register a new vendor. |
| POST   | `/users/signup/contributor`   | Register a new contributor. |
| POST   | `/users/login`                | Cookie-based login for all user types. |
| POST   | `/users/logout`               | Logout and clear the session. |
| GET	    | `/search/nearby`	           |The primary search endpoint. Finds items in shops near a given latitude and longitude.|
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
├── docker-compose.yml # Dev stack (FastAPI + PostGIS + Typesense)
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
```

🧪 Testing
```bash
docker-compose exec backend pytest
```

🔮 Roadmap
Admin Dashboard: A simple interface for shop owners to manage their inventory.
Caching Layer: Implement Redis for caching frequently accessed data.
Notification : Kafka and websocket
Real-Time Updates: Use WebSockets for live stock updates.
QR Code Integration: Allow users to quickly find a shop by scanning a QR code.


🤝 Contributing
Pull requests and ideas are welcome! Please keep contributions modular and follow the naming/style conventions already established in the repo.

📜 License
MIT © Rahul Roy
🙏 Acknowledgements
FastAPI,PostgreSQL + PostGIS,SQLAlchemy Models & Alembic
Fellow devs and open-source contributors.
