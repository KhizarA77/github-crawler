import psycopg2
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.config import DB_CONFIG

schema_sql = """
CREATE TABLE IF NOT EXISTS repositories (
    repo_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    owner TEXT NOT NULL,
    stars INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def main():
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    print("Creating schema...")
    cur.execute(schema_sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Schema setup complete.")

if __name__ == "__main__":
    main()
