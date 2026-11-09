# Issue Tracker CLI

[![tests](https://github.com/Enricosi/Issue-Tracker/actions/workflows/tests.yml/badge.svg)](https://github.com/Enricosi/Issue-Tracker/actions/workflows/tests.yml)

**English** · [Español](README.es.md)

A command-line tool to manage issues and developers, backed by MySQL.

Built with Python, `argparse` and PyMySQL. All queries are parameterized, writes are committed explicitly, and business rules (for example, only closed issues can be deleted) are enforced in code and backed by database constraints.

## Requirements

- Python 3.8+
- MySQL 8.0+

## Setup

```bash
pip install -r requirements.txt

mysql -u <user> -p -e "CREATE DATABASE issue_tracker_db"
mysql -u <user> -p issue_tracker_db < schema.sql

cp .env.example .env   # then fill in your own values
```

```env
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=issue_tracker_db
```

## Usage

```bash
python issue_tracker.py <command> [arguments]
```

## Commands

### Issues

| Command | What it does |
|---|---|
| `list_issues [-s STATUS] [-u USERNAME]` | List issues, optionally filtered by status (`open`, `in_progress`, `closed`) and/or assigned developer |
| `add_issue TITLE PRIORITY [-u USERNAME] [-p CAUSE]` | Create an issue. Priority is `1`, `2` or `3` (3 = highest) |
| `delete_issue ID` | Delete an issue. Only `closed` issues can be deleted |
| `change_status ID NEW_STATUS` | Change the status. Moving to `closed` records the close date |
| `reassign_issue ID USERNAME` | Assign the issue to another developer |

```bash
python issue_tracker.py add_issue "Login fails" 2 -u john -p "Expired token"
python issue_tracker.py list_issues -u john -s in_progress
python issue_tracker.py change_status 5 closed
```

### Developers

| Command | What it does |
|---|---|
| `list_developers [-u USERNAME]` | List developers with their number of active issues |
| `add_developer USERNAME FIRST_NAME [-l LAST_NAME]` | Register a developer (username must be unique) |
| `remove_developer USERNAME` | Remove a developer. Not allowed while they have issues assigned |

```bash
python issue_tracker.py add_developer john John -l Doe
python issue_tracker.py list_developers
```

## Data model

Two tables: `developer` and `issue`. An issue optionally references a developer (foreign key). `CHECK` constraints keep `status` within `open`, `in_progress`, `closed` and `priority` between 1 and 3. See [`schema.sql`](schema.sql).

## Tests

The tests use a fake database connection, so they run without MySQL:

```bash
pip install -r requirements-dev.txt
pytest
```

They run automatically on every push and pull request with GitHub Actions.

## Project structure

```
issue_tracker.py       entry point: parse args, open the connection, dispatch
parser.py              argparse subcommands
dispatch.py            maps each command to its handler
commands_issues.py     issue commands
commands_developer.py  developer commands
connect.py             reads .env and opens the MySQL connection
exceptions.py          IssueTrackerError for expected business-rule errors
schema.sql             database schema
tests/                 pytest suite
```
