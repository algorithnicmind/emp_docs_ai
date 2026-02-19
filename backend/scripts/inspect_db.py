
import asyncio
import sys
import os
from sqlalchemy import text

# Add parent directory to path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import async_session, engine

async def inspect_db():
    async with async_session() as db:
        print("\n📊 Database Tables & Row Counts:")
        print("="*40)
        
        # Get all table names
        result = await db.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.scalars().all()
        
        for table in tables:
            if table == "alembic_version": continue
            count = await db.execute(text(f"SELECT COUNT(*) FROM {table}"))
            print(f"• {table}: {count.scalar()} rows")

        print("\n👥 Users:")
        print("="*40)
        users = await db.execute(text("SELECT email, role, name FROM users"))
        for u in users:
            print(f"- {u.name} ({u.email}) - {u.role}")

        print("\n📄 Documents:")
        print("="*40)
        docs = await db.execute(text("SELECT title, source, status FROM documents"))
        rows = docs.fetchall()
        if not rows:
            print("(No documents found)")
        for d in rows:
            print(f"- {d.title} [{d.source}] ({d.status})")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(inspect_db())
    except Exception as e:
        print(f"Error: {e}")
