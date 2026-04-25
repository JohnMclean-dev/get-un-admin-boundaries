"""
Database connection utilities using SQLAlchemy.
"""

import logging
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def build_db_url() -> str:
    """
    Build a PostgreSQL connection URL from environment variables.
    """
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "postgres")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def create_db_engine(echo: bool = False) -> Engine:
    """
    Create a SQLAlchemy engine with sensible defaults.
    """
    db_url = build_db_url()

    logger.info(f"Creating database engine for host={os.getenv('DB_HOST')} db={os.getenv('DB_NAME')}")

    engine = create_engine(
        db_url,
        echo=echo,
        pool_pre_ping=True,   # avoids stale connections
        pool_size=5,
        max_overflow=10,
    )

    return engine


def test_connection(engine: Engine) -> bool:
    """
    Test database connectivity.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        
        with engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology;"))
        logger.info("Check and add PostGIS extension if uninstalled")

        return True

    except Exception as e:
        logger.exception("Database connection failed")
        return False


def get_connection(engine: Engine):
    """
    Context manager wrapper for a DB connection.
    """
    return engine.begin()