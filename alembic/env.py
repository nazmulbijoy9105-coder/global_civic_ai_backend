import sys
import os
from sqlalchemy import create_engine
from alembic import context

# Ensure Alembic can find your backend package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.database import Base
import backend.app.models  # ensure models are imported so Alembic sees them

# Use DATABASE_URL from environment, fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)

# Tell Alembic what metadata to look at
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()