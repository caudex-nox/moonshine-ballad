import os
import sys
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD_RAW = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT", "4000")
DB_NAME = os.getenv("DB_NAME", "moonshine_ballad")

# Validar que existan las credenciales mínimas antes de intentar conectar
if not USER or not PASSWORD_RAW or not HOST:
    print("❌ Error: Faltan variables de entorno requeridas en el archivo .env (DB_USER, DB_PASSWORD, DB_HOST).")
    sys.exit(1)

PASSWORD = quote_plus(PASSWORD_RAW)

# Conexión inicial a la BD 'test' para ejecutar la creación de la BD y sus tablas
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/test?ssl_ca=/etc/ssl/certs/ca-certificates.crt"

engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {"ca": "/etc/ssl/certs/ca-certificates.crt"}},
    pool_pre_ping=True
)

def ejecutar_schema():
    print("⏳ Conectando a TiDB Cloud...")
    try:
        with open("db/schema.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

        with engine.connect() as connection:
            statements = [s.strip() for s in sql_script.split(";") if s.strip()]
            for statement in statements:
                connection.execute(text(statement))
            connection.commit()

        print("✅ Base de datos y estructuras creadas correctamente en TiDB Cloud.")

        # Verificar tablas creadas en la base de datos recién inicializada
        url_mb = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?ssl_ca=/etc/ssl/certs/ca-certificates.crt"
        engine_mb = create_engine(url_mb, connect_args={"ssl": {"ca": "/etc/ssl/certs/ca-certificates.crt"}})
        with engine_mb.connect() as conn:
            result = conn.execute(text("SHOW TABLES;"))
            tablas = [row[0] for row in result]
            print("📋 Tablas creadas:", tablas)

    except Exception as e:
        print("❌ Error al ejecutar el script:", e)

if __name__ == "__main__":
    ejecutar_schema()