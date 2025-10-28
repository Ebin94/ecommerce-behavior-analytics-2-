"""
Utility functions for database connectivity.

If a `DATABASE_URL` environment variable is set it will be used for the SQLAlchemy
engine; otherwise the default is a local SQLite database (`ecommerce.db`).
"""
import os
from sqlalchemy import create_engine


def get_engine():
    """Return a SQLAlchemy engine based on the DATABASE_URL env var or a default."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Fallback to a local SQLite database in the project root
        db_url = 'sqlite:///ecommerce.db'
    return create_engine(db_url, echo=False)