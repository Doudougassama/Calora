# Calorie Tracker

A small, self-hosted calorie & macro tracker inspired by apps like MyFitnessPal —
built from scratch (Flask + SQLite + vanilla JS), not a copy of anyone's
proprietary code. Everything runs locally; your data stays in a SQLite file
on your own machine.

## Features

- **BMR / TDEE calculator** — Mifflin-St Jeor equation, adjustable by
  activity level, with a daily calorie goal based on lose / maintain / gain.
- **Food search + log** — seeded with ~80 common foods (fruits, veg,
  proteins, grains, dairy, fast food, snacks). Search, pick a serving count,
  assign to a meal (breakfast/lunch/dinner/snack), and log it.
- **Custom foods** — anything not in the seed list can be added by hand
  (name, serving size, calories, protein/carbs/fat) and is saved for reuse.
- **Daily summary** — calories eaten vs. goal, remaining calories, and a
  protein/carb/fat breakdown.
- **Date navigation** — step backward/forward to log or review any day.

## Requirements

- Python 3.9+
- No other services — SQLite ships with Python's standard library.

## Setup

```bash
cd calorie-tracker
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

The first run creates `instance/calorie_tracker.db` and seeds it with the
starter food list automatically — nothing else to configure.

## Project structure

```
calorie-tracker/
├── app.py            # Flask routes / API
├── database.py        # SQLite schema + connection helper
├── seed_data.py        # Starter food list (~80 items)
├── requirements.txt
├── templates/
│   └── index.html      # Single-page UI
├── static/
│   ├── style.css
│   └── app.js          # Fetch calls to the API, all UI logic
└── instance/            # Created at runtime, holds the .db file (git-ignored)
```

## API reference

| Method | Route              | Purpose                                   |
|--------|---------------------|--------------------------------------------|
| GET    | `/api/foods?q=`     | Search foods by name                      |
| POST   | `/api/foods`        | Add a custom food                         |
| GET    | `/api/log?date=`    | List log entries for a date               |
| POST   | `/api/log`          | Add a log entry (by `food_id` or ad hoc)  |
| DELETE | `/api/log/<id>`     | Remove a log entry                        |
| GET    | `/api/summary?date=`| Daily totals + remaining calories         |
| GET    | `/api/profile`      | Get saved profile/goal                    |
| POST   | `/api/profile`      | Save profile, recompute BMR/TDEE/goal     |

## A note on how this was verified

This was built and code-reviewed carefully (route names, request payloads,
and DOM element IDs were all cross-checked between `app.js`, `index.html`,
and `app.py`), but it was **not run end-to-end** in a live Python
environment before being handed to you — the build sandbox didn't have a
working shell at the time. Please run it locally and sanity-check it (add a
food, save a profile, delete an entry) before you rely on it. If anything
breaks, the error will show up in the terminal running `python app.py` and
in the browser console (F12).

## Push to your own GitHub

From inside the `calorie-tracker` folder:

```bash
git init
git add .
git commit -m "Initial commit: calorie tracker (Flask + SQLite)"
```

Then create an empty repository on GitHub (no README/license, so it stays
empty) at **https://github.com/new**, and push:

```bash
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

If you'd rather use SSH:

```bash
git remote add origin git@github.com:<your-username>/<repo-name>.git
git push -u origin main
```

## License

No license file is included — add one (MIT is a common default for small
personal projects) if you plan to make the repo public.
