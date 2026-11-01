import os
import sys
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD_RAW = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT", "4000")
DB_NAME = os.getenv("DB_NAME", "moonshine_ballad")

if not all([USER, PASSWORD_RAW, HOST]):
    print("❌ Error: Variables de conexión incompletas en .env")

PASSWORD = quote_plus(PASSWORD_RAW) if PASSWORD_RAW else ""

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?ssl_ca=/etc/ssl/certs/ca-certificates.crt"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": "/etc/ssl/certs/ca-certificates.crt"
        }
    },
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()