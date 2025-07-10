# 🧭 Hyperlocal Shop Finder – Backend

A location-based backend service that helps users discover nearby shops (within a 2–5 meter radius) that stock specific items — like “Maggie”, “batteries”, or “coffee sachets” — with real-time availability, quantity, and shop status.

This backend is designed with extensibility, scalability, and modularity in mind — ideal for production-grade deployments as well as developer onboarding.

---

## ✨ Features

- 🔍 **Geo-based Search API** — find shops within 2–5 meters that have a given item
- 🛒 **Inventory Tracking** — per shop, per item, with real-time quantity updates
- 📍 **PostGIS Spatial Queries** — accurate distance-based shop lookup
- 🧾 **Modular API Structure** — RESTful and versioned (`/api/v1`)
- 🔐 **Cookie-based Auth** — optional login for users, mandatory for shop owners
- 🧱 **Clean Architecture** — with layered services, reusable schema, and test coverage
- 🐳 **Docker-Ready** — includes dev containers with PostgreSQL + PostGIS

---

## 🚀 API Overview (Might change with time)

| Method | Endpoint                        | Description                                |
|--------|----------------------------------|--------------------------------------------|
| `POST` | `/auth/register`                | Register a new user or shop owner          |
| `POST` | `/auth/login`                   | Cookie-based login                         |
| `POST` | `/auth/logout`                  | Logout and clear session                   |
| `GET`  | `/search?lat=&lon=&item=`       | Find shops within 2–5m that stock an item  |
| `POST` | `/shops/`                       | Create a shop (requires owner auth)        |
| `GET`  | `/shops/{id}`                   | Get shop details                           |
| `PATCH`| `/shops/{id}/status`            | Toggle open/closed status (owner-only)     |
| `POST` | `/items/`                       | Add new items to the system                |
| `POST` | `/inventory/`                   | Update quantity of an item in a shop       |

---

## 🗂️ Project Structure



NEARBUY/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app, routers, middleware

│   ├── api/                        # All route logic, organized by version
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── auth/
│   │   │   │   │   ├── login.py    # /auth/login
│   │   │   │   │   ├── register.py # /auth/register
│   │   │   │   │   ├── logout.py   # /auth/logout
│   │   │   │   ├── users.py        # general user info
│   │   │   │   ├── shops.py        # create, get, update shop
│   │   │   │   ├── items.py        # item CRUD
│   │   │   │   ├── inventory.py    # shop's stock management
│   │   │   │   ├── search.py       # /search endpoint
│   │   │   │   └── status.py       # toggle shop open/closed

│   ├── core/                       # App-level core logic/config
│   │   ├── config.py               # .env parser, settings
│   │   ├── security.py             # password hashing, auth utils
│   │   ├── session.py              # cookie session manager
│   │   └── dependencies.py         # Depends() logic extract

│   ├── db/
│   │   ├── base.py                 # for Alembic + Base metadata
│   │   ├── session.py              # SQLAlchemy session connection
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── shop.py
│   │   │   ├── item.py
│   │   │   ├── inventory.py
│   │   └── schemas/
│   │       ├── user.py
│   │       ├── shop.py
│   │       ├── item.py
│   │       ├── inventory.py

│   ├── services/
│   │   ├── auth_service.py         # login, register logic
│   │   ├── shop_service.py         # create/update/fetch shop logic
│   │   ├── item_service.py         # item creation/fetch
│   │   ├── inventory_service.py    # add/modify quantity
│   │   └── search_service.py       # PostGIS search logic

│   ├── utils/
│   │   ├── geo.py                  # Haversine, PostGIS helpers
│   │   └── validators.py           # item/lat-lon validation, etc.

│   └── tests/                      # Unit & integration tests
│       ├── unit/
│       ├── integration/
│       └── factories/              # test data factories

├── scripts/
│   ├── seed_data.py                # dummy data for shops, items, inventory
│   ├── test_geo_queries.py         # spatial query tester

├── alembic/                        # DB migrations
├── Dockerfile
├── docker-compose.yml             # Postgres + FastAPI dev env
├── .env                            # secrets and config
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
Pull requests and ideas welcome! Please keep contributions modular and follow naming/style conventions already established in the repo.

📜 License
MIT © Rahul Roy

🙏 Acknowledgements
FastAPI

PostgreSQL + PostGIS

SQLAlchemy & Alembic

Fellow devs and open-source contributors

