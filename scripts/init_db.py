"""Run this script to create database tables.
Usage: python scripts/init_db.py

This script ensures the project root is on sys.path so local imports like
`app.core.db` work when the script is executed directly.
"""
import sys
from pathlib import Path

# Add project root to sys.path so `app` package can be imported
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from app.core.db import init_db


if __name__ == "__main__":
    init_db()
    print("Database tables created (if they did not already exist).")
