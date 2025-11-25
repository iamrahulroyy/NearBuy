import sys
import os
import asyncio
import uuid
from sqlmodel import Session, select, create_engine

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.models.user import USER, UserRole
from app.helpers.loginHelper import security
from app.helpers.variables import DATABASE_URL

async def create_admin_user():
    print("Connecting to database...")
    engine = create_engine(DATABASE_URL)
    
    admin_email = "admin@nearbuy.com"
    admin_password = "AdminPassword@123"
    
    with Session(engine) as session:
        # Check if admin already exists
        statement = select(USER).where(USER.email == admin_email)
        existing_user = session.exec(statement).first()
        
        if existing_user:
            print(f"Admin user already exists: {admin_email}")
            # Optional: Update role to ADMIN if it's not
            if existing_user.role != UserRole.ADMIN and existing_user.role != UserRole.SUPER_ADMIN:
                print("Updating existing user to ADMIN role...")
                existing_user.role = UserRole.ADMIN
                session.add(existing_user)
                session.commit()
                print("User updated.")
            return

        print(f"Creating new admin user: {admin_email}")
        new_admin = USER(
            id=uuid.uuid4(),
            email=admin_email,
            password=security().hash_password(admin_password),
            fullName="System Admin",
            role=UserRole.ADMIN
        )
        
        session.add(new_admin)
        session.commit()
        print("Admin user created successfully!")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")

if __name__ == "__main__":
    asyncio.run(create_admin_user())
