# -*- coding: utf-8 -*-
"""
Calorie Tracker -- a small self-hosted MyFitnessPal-style app.

Flask + SQLite, no external services. Run with:
    python app.py
then open http://127.0.0.1:5000
"""
from datetime import datetime

from flask import Flask, jsonify, render_template, request

from database import get_connection, init_db, today_str

app = Flask(__name__)

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,      # little or no exercise
    "light": 1.375,        # light exercise 1-3 days/week
    "moderate": 1.55,      # moderate exercise 3-5 days/week
    "active": 1.725,       # hard exercise 6-7 days/week
    "very_active": 1.9,    # very hard exercise & physical job
}
VALID_GOALS = {"lose", "maintain", "gain"}
VALID_SEX = {"male", "female"}
MIN_SAFE_CALORIES = 1200


def error(message, status=400):
    return jsonify({"error": message}), status


def compute_bmr(sex, age, height_cm, weight_kg):
    """Mifflin-St Jeor equation."""
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if sex == "male" else base - 161


def compute_calorie_goal(tdee, goal):
    if goal == "lose":
        return max(MIN_SAFE_CALORIES, tdee - 500)
    if goal == "gain":
        return tdee + 500
    return tdee


# ---------------------------------------------------------------- pages ---
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------------------------------------------------- foods ---
@app.route("/api/foods", methods=["GET"])
def search_foods():
    q = request.args.get("q", "").strip()
    conn = get_connection()
    try:
        if q:
            rows = conn.execute(
                """SELECT * FROM foods WHERE name LIKE ?
                   ORDER BY is_custom DESC, name ASC LIMIT 25""",
                (f"%{q}%",),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM foods ORDER BY is_custom DESC, name ASC LIMIT 25"
            ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route("/api/foods", methods=["POST"])
def add_food():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    serving_desc = (data.get("serving_desc") or "1 serving").strip()

    if not name:
        return error("A food name is required.")

    try:
        calories = float(data.get("calories", 0))
        protein_g = float(data.get("protein_g", 0) or 0)
        carbs_g = float(data.get("carbs_g", 0) or 0)
        fat_g = float(data.get("fat_g", 0) or 0)
    except (TypeError, ValueError):
        return error("Calories and macros must be numbers.")

    if calories < 0 or protein_g < 0 or carbs_g < 0 or fat_g < 0:
        return error("Calories and macros can't be negative.")

    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO foods (name, serving_desc, calories, protein_g, carbs_g, fat_g, is_custom)
               VALUES (?, ?, ?, ?, ?, ?, 1)""",
            (name, serving_desc, calories, protein_g, carbs_g, fat_g),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM foods WHERE id = ?", (cur.lastrowid,)).fetchone()
        return jsonify(dict(row)), 201
    finally:
        conn.close()


# ------------------------------------------------------------------- log ---
@app.route("/api/log", methods=["GET"])
def get_log():
    log_date = request.args.get("date", today_str())
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT * FROM log_entries WHERE log_date = ?
               ORDER BY CASE meal
                   WHEN 'breakfast' THEN 0
                   WHEN 'lunch' THEN 1
                   WHEN 'dinner' THEN 2
                   ELSE 3 END, created_at ASC""",
            (log_date,),
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route("/api/log", methods=["POST"])
def add_log_entry():
    data = request.get_json(silent=True) or {}
    log_date = (data.get("date") or today_str()).strip()
    meal = (data.get("meal") or "snack").strip().lower()
    if meal not in {"breakfast", "lunch", "dinner", "snack"}:
        return error("meal must be one of breakfast, lunch, dinner, snack.")

    conn = get_connection()
    try:
        food_id = data.get("food_id")
        if food_id:
            try:
                servings = float(data.get("servings", 1) or 1)
            except (TypeError, ValueError):
                return error("servings must be a number.")
            if servings <= 0:
                return error("servings must be greater than 0.")

            food = conn.execute("SELECT * FROM foods WHERE id = ?", (food_id,)).fetchone()
            if not food:
                return error("That food no longer exists.", 404)

            food_name = food["name"]
            calories = food["calories"] * servings
            protein_g = food["protein_g"] * servings
            carbs_g = food["carbs_g"] * servings
            fat_g = food["fat_g"] * servings
        else:
            # Ad-hoc entry not tied to a saved food row.
            food_name = (data.get("food_name") or "").strip()
            if not food_name:
                return error("food_id or food_name is required.")
            try:
                servings = 1.0
                calories = float(data.get("calories", 0))
                protein_g = float(data.get("protein_g", 0) or 0)
                carbs_g = float(data.get("carbs_g", 0) or 0)
                fat_g = float(data.get("fat_g", 0) or 0)
            except (TypeError, ValueError):
                return error("Calories and macros must be numbers.")
            food_id = None

        cur = conn.execute(
            """INSERT INTO log_entries
               (log_date, meal, food_id, food_name, servings, calories, protein_g, carbs_g, fat_g, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                log_date, meal, food_id, food_name, servings,
                calories, protein_g, carbs_g, fat_g,
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM log_entries WHERE id = ?", (cur.lastrowid,)).fetchone()
        return jsonify(dict(row)), 201
    finally:
        conn.close()


@app.route("/api/log/<int:entry_id>", methods=["DELETE"])
def delete_log_entry(entry_id):
    conn = get_connection()
    try:
        cur = conn.execute("DELETE FROM log_entries WHERE id = ?", (entry_id,))
        conn.commit()
        if cur.rowcount == 0:
            return error("Log entry not found.", 404)
        return jsonify({"deleted": entry_id})
    finally:
        conn.close()


@app.route("/api/summary", methods=["GET"])
def get_summary():
    log_date = request.args.get("date", today_str())
    conn = get_connection()
    try:
        totals = conn.execute(
            """SELECT
                   COALESCE(SUM(calories), 0) AS calories,
                   COALESCE(SUM(protein_g), 0) AS protein_g,
                   COALESCE(SUM(carbs_g), 0) AS carbs_g,
                   COALESCE(SUM(fat_g), 0) AS fat_g
               FROM log_entries WHERE log_date = ?""",
            (log_date,),
        ).fetchone()

        profile = conn.execute("SELECT * FROM profile WHERE id = 1").fetchone()
        calorie_goal = profile["calorie_goal"] if profile else None

        result = dict(totals)
        result["date"] = log_date
        result["calorie_goal"] = calorie_goal
        result["remaining"] = (calorie_goal - result["calories"]) if calorie_goal is not None else None
        return jsonify(result)
    finally:
        conn.close()


# --------------------------------------------------------------- profile ---
@app.route("/api/profile", methods=["GET"])
def get_profile():
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM profile WHERE id = 1").fetchone()
        return jsonify(dict(row) if row else None)
    finally:
        conn.close()


@app.route("/api/profile", methods=["POST"])
def save_profile():
    data = request.get_json(silent=True) or {}
    sex = (data.get("sex") or "").strip().lower()
    activity_level = (data.get("activity_level") or "").strip().lower()
    goal = (data.get("goal") or "").strip().lower()

    if sex not in VALID_SEX:
        return error("sex must be 'male' or 'female'.")
    if activity_level not in ACTIVITY_MULTIPLIERS:
        return error(f"activity_level must be one of {sorted(ACTIVITY_MULTIPLIERS)}.")
    if goal not in VALID_GOALS:
        return error(f"goal must be one of {sorted(VALID_GOALS)}.")

    try:
        age = int(data.get("age"))
        height_cm = float(data.get("height_cm"))
        weight_kg = float(data.get("weight_kg"))
    except (TypeError, ValueError):
        return error("age, height_cm and weight_kg must be numbers.")

    if not (10 <= age <= 120):
        return error("age must be between 10 and 120.")
    if not (100 <= height_cm <= 250):
        return error("height_cm must be between 100 and 250.")
    if not (30 <= weight_kg <= 400):
        return error("weight_kg must be between 30 and 400.")

    bmr = compute_bmr(sex, age, height_cm, weight_kg)
    tdee = bmr * ACTIVITY_MULTIPLIERS[activity_level]
    calorie_goal = compute_calorie_goal(tdee, goal)

    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO profile (id, sex, age, height_cm, weight_kg, activity_level, goal, bmr, tdee, calorie_goal)
               VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                   sex=excluded.sex, age=excluded.age, height_cm=excluded.height_cm,
                   weight_kg=excluded.weight_kg, activity_level=excluded.activity_level,
                   goal=excluded.goal, bmr=excluded.bmr, tdee=excluded.tdee,
                   calorie_goal=excluded.calorie_goal""",
            (sex, age, height_cm, weight_kg, activity_level, goal, bmr, tdee, calorie_goal),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM profile WHERE id = 1").fetchone()
        return jsonify(dict(row))
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
else:
    # Also make sure the DB exists when run under a WSGI server (e.g. gunicorn).
    init_db()
