import psycopg2
from src.config import load_config

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
    config = load_config()
    conn = psycopg2.connect(
        host=config.postgres_host,
        port=config.postgres_port,
        dbname=config.postgres_db,
        user=config.postgres_user,
        password=config.postgres_password
    )
    cur = conn.cursor()
    print("Creating schema...")
    cur.execute(schema_sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Schema setup complete.")

if __name__ == "__main__":
    main()
