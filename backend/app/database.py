from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use your Render PostgreSQL URL here
SQLALCHEMY_DATABASE_URL = "postgresql://global_civic_ai_db_user:lVoqemzHJhpgUrYFg2DQXxVTmtjFo89U@dpg-d67mb3ur433s73f9q660-a.oregon-postgres.render.com/global_civic_ai_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()