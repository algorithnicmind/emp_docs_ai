
import asyncio
import sys
import os

# Add parent directory to path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import async_session, engine, Base
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed():
    print("🌱 Seeding database...")
    
    # Create tables if not exist (redundant if main.py ran, but safe)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        # Check if admin exists
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.email == "admin@company.com"))
        if result.scalar_one_or_none():
            print("✅ Admin user already exists")
            return

        # Create Admin User
        admin = User(
            name="Admin User",
            email="admin@company.com",
            password_hash=pwd_context.hash("admin123"),
            role="admin",
            department="all"
        )
        db.add(admin)
        
        # Create General User
        user = User(
            name="General User",
            email="user@company.com",
            password_hash=pwd_context.hash("user123"),
            role="general",
            department="engineering"
        )
        db.add(user)
        
        await db.commit()
        print("✅ Created users:")
        print("   - admin@company.com / admin123")
        print("   - user@company.com / user123")

if __name__ == "__main__":
    asyncio.run(seed())
