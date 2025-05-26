# code-challenge-week2
# Authors, Articles, and Magazines

A  Python + SQL project that models relationships between authors, articles, and magazines using object-oriented programming and  SQL.

## Project Structure
code-challenge/
├── lib/
│ ├── models/
│ ├── db/
│ ├── debug.py
├── scripts/
├── tests/
├── README.md



##  Features

- Create and save Authors, Magazines, and Articles.
- Link Articles to both an Author and a Magazine.
- Get all articles by an Author.
- Get all contributors of a Magazine.
- Get all topic areas an Author has written for.
- Find authors who contributed more than 2 articles to a magazine.

## Setup Instructions

1. **Install Python 3.8+**  
2. **Install dependencies** (optional):
   ```bash
   pip install -r requirements.txt
3. **Create the database:**

python scripts/setup_db.py



##  Files
  - lib/models/ – Contains the Author, Article, and Magazine classes.

- lib/db/ – Contains the SQLite schema, seed data, and database connection.

- scripts/ – Scripts to set up and interact with the database.

- tests/ – Unit tests using pytest.

