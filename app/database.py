from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": settings.DB_SSL_CA
        }
    },
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def ensure_schema_compatibility():
    with engine.begin() as connection:
        connection.execute(text(
            "ALTER TABLE productos ADD COLUMN IF NOT EXISTS imagen_url VARCHAR(500)"
        ))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()