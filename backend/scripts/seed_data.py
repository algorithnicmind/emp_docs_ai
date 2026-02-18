"""
Seed Data Script
==================
Populates the database with sample data for testing:
- Admin user
- Sample documents with chunks
"""

import asyncio
import uuid
from datetime import datetime

from sqlalchemy import select
from passlib.context import CryptContext

# Add parent dir to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import async_session, engine, Base
from app.models.user import User
from app.models.document import Document
from app.models.chunk import Chunk

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SAMPLE_USERS = [
    {
        "name": "Admin User",
        "email": "admin@company.com",
        "password": "admin123",
        "role": "admin",
        "department": "general",
    },
    {
        "name": "HR Manager",
        "email": "hr@company.com",
        "password": "hr123456",
        "role": "hr",
        "department": "hr",
    },
    {
        "name": "Engineer",
        "email": "engineer@company.com",
        "password": "eng123456",
        "role": "engineering",
        "department": "engineering",
    },
    {
        "name": "Finance Lead",
        "email": "finance@company.com",
        "password": "fin123456",
        "role": "finance",
        "department": "finance",
    },
    {
        "name": "Employee",
        "email": "employee@company.com",
        "password": "emp123456",
        "role": "general",
        "department": "general",
    },
]


async def seed():
    """Seed the database with sample data."""

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Seed users
        for user_data in SAMPLE_USERS:
            result = await session.execute(
                select(User).where(User.email == user_data["email"])
            )
            if result.scalar_one_or_none():
                print(f"  ⏭️  User '{user_data['email']}' already exists")
                continue

            user = User(
                name=user_data["name"],
                email=user_data["email"],
                password_hash=pwd_context.hash(user_data["password"]),
                role=user_data["role"],
                department=user_data["department"],
            )
            session.add(user)
            print(f"  ✅ Created user: {user_data['name']} ({user_data['role']})")

        await session.commit()

    print("\n🎉 Seed data loaded successfully!")
    print("\n📋 Test accounts:")
    print("  ┌──────────────────────┬──────────────────┬──────────────┐")
    print("  │ Email                │ Password         │ Role         │")
    print("  ├──────────────────────┼──────────────────┼──────────────┤")
    for u in SAMPLE_USERS:
        print(f"  │ {u['email']:<20} │ {u['password']:<16} │ {u['role']:<12} │")
    print("  └──────────────────────┴──────────────────┴──────────────┘")


if __name__ == "__main__":
    print("🌱 Seeding database...")
    asyncio.run(seed())
