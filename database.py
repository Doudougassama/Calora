# -*- coding: utf-8 -*-
"""
Thin SQLite data-access layer for the calorie tracker.

Kept dependency-free (standard-library `sqlite3` only) so the whole app
runs with nothing installed but Flask itself.
"""
import os
import sqlite3
from datetime import date

from seed_data import FOODS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "calorie_tracker.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    serving_desc TEXT NOT NULL,
    calories REAL NOT NULL,
    protein_g REAL NOT NULL DEFAULT 0,
    carbs_g REAL NOT NULL DEFAULT 0,
    fat_g REAL NOT NULL DEFAULT 0,
    is_custom INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS log_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date TEXT NOT NULL,
    meal TEXT NOT NULL,
    food_id INTEGER,
    food_name TEXT NOT NULL,
    servings REAL NOT NULL,
    calories REAL NOT NULL,
    protein_g REAL NOT NULL DEFAULT 0,
    carbs_g REAL NOT NULL DEFAULT 0,
    fat_g REAL NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (food_id) REFERENCES foods (id)
);

CREATE TABLE IF NOT EXISTS profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    sex TEXT NOT NULL,
    age INTEGER NOT NULL,
    height_cm REAL NOT NULL,
    weight_kg REAL NOT NULL,
    activity_level TEXT NOT NULL,
    goal TEXT NOT NULL,
    bmr REAL NOT NULL,
    tdee REAL NOT NULL,
    calorie_goal REAL NOT NULL
);
"""


def get_connection():
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if missing and seed the food list on first run."""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()

        count = conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0]
        if count == 0:
            conn.executemany(
                """INSERT INTO foods
                   (name, serving_desc, calories, protein_g, carbs_g, fat_g, is_custom)
                   VALUES (?, ?, ?, ?, ?, ?, 0)""",
                FOODS,
            )
            conn.commit()
    finally:
        conn.close()


def today_str():
    return date.today().isoformat()
