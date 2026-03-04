from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database URL (must be set in Render environment variables)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "❌ DATABASE_URL is not set!\n"
        "Please add DATABASE_URL to your Render environment variables:\n"
        "1. Go to Render dashboard → Your Service\n"
        "2. Click 'Environment' tab\n"
        "3. Add: DATABASE_URL = your_postgresql_connection_string\n"
        "Example: postgresql://user:pass@host:5432/dbname"
    )

# SQLAlchemy engine with connection pooling for Render
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using them
    pool_recycle=3600,   # Recycle connections every hour
    echo=False,          # Set True for debugging SQL queries
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test database connection on startup
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Set up connection parameters"""
    try:
        dbapi_conn.connection.set_isolation_level(0)
    except AttributeError:
        pass
