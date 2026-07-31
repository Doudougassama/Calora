<div align="center">

# Calora

**A calorie & macro tracker built from scratch — Flask, SQLite, vanilla JS.**

[![Live Demo](https://img.shields.io/badge/demo-live-2f9e6e?style=flat-square)](https://calora-qa13.onrender.com/)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

**[Try it live →](https://calora-qa13.onrender.com/)**

</div>

---

## What it is

Calora is a self-built, MyFitnessPal-style calorie and macro tracker —
not a copy of anyone's proprietary code, built from scratch with a Flask
API, a SQLite database, and a single-page vanilla-JS frontend. No
framework build step, no external services, no tracking.

## Features

- **BMR / TDEE calculator** — Mifflin-St Jeor equation, adjustable by
  activity level, with a daily calorie goal for losing, maintaining, or
  gaining weight.
- **Food search & logging** — ~80 seeded common foods across fruits,
  vegetables, proteins, grains, dairy, fast food, and snacks. Search,
  choose a serving count, assign to a meal, and log it.
- **Custom foods** — anything missing can be added by hand and is saved
  for future searches.
- **Daily summary** — calories eaten vs. goal, remaining calories, and a
  protein / carb / fat breakdown with visual bars.
- **Date navigation** — step backward and forward to log or review any
  day.

## Tech stack

| Layer     | Choice                                   |
|-----------|-------------------------------------------|
| Backend   | Flask (Python), REST-style JSON API        |
| Database  | SQLite (`sqlite3`, standard library only)  |
| Frontend  | Vanilla HTML / CSS / JS — no framework      |
| Hosting   | [Render](https://render.com) (free tier)    |

## Run it locally

```bash
git clone https://github.com/Doudougassama/Calora.git
cd Calora
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**. The first run creates
`instance/calorie_tracker.db` and seeds it automatically — nothing else
to configure.

## Project structure

```
Calora/
├── app.py            # Flask routes / API
├── database.py         # SQLite schema + connection helper
├── seed_data.py         # Starter food list (~80 items)
├── requirements.txt
├── templates/
│   └── index.html       # Single-page UI
├── static/
│   ├── style.css
│   └── app.js            # All frontend logic, calls the API
└── instance/              # Created at runtime, holds the .db file (git-ignored)
```

## API reference

| Method | Route                | Purpose                                    |
|--------|------------------------|----------------------------------------------|
| GET    | `/api/foods?q=`       | Search foods by name                        |
| POST   | `/api/foods`          | Add a custom food                           |
| GET    | `/api/log?date=`      | List log entries for a date                 |
| POST   | `/api/log`            | Add a log entry (by `food_id` or ad hoc)    |
| DELETE | `/api/log/<id>`       | Remove a log entry                          |
| GET    | `/api/summary?date=`  | Daily totals + remaining calories           |
| GET    | `/api/profile`        | Get saved profile / goal                    |
| POST   | `/api/profile`        | Save profile, recompute BMR / TDEE / goal   |

## Deployment notes

Deployed on Render's free tier: `pip install -r requirements.txt` as the
build command, `gunicorn --bind 0.0.0.0:$PORT app:app` as the start
command. The free tier has an ephemeral filesystem, so the SQLite file
resets on redeploys and periods of inactivity — the seeded food list
repopulates automatically, but logged entries won't survive a restart.
For persistent data, attach a Render disk or point `database.py` at a
managed Postgres instance instead.

## License

MIT — see [LICENSE](LICENSE).
