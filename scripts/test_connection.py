import psycopg2
from src.config import load_config

print("Connecting to PostgreSQL...")
config = load_config()
conn = psycopg2.connect(
    host=config.postgres_host,
    port=config.postgres_port,
    dbname=config.postgres_db,
    user=config.postgres_user,
    password=config.postgres_password
)
print("Connected successfully:", conn.get_dsn_parameters()["dbname"])
conn.close()