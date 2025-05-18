from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import psycopg2
from pgvector.psycopg2 import register_vector
from sqlalchemy import event

# Configure Neon DB connection
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

# Enable pgvector extension
def setup_vector_extension(dbapi_connection, connection_record):
    register_vector(dbapi_connection)
    cursor = dbapi_connection.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
    cursor.close()

event.listen(engine, "connect", setup_vector_extension)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 