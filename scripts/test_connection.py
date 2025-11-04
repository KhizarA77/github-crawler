import psycopg2
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
print("Connected successfully:", conn.get_dsn_parameters()["dbname"])
conn.close()