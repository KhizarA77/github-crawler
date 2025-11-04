import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.postgres_host = os.getenv("POSTGRES_HOST", "localhost")
        self.postgres_port = os.getenv("POSTGRES_PORT", "5432")
        self.postgres_db = os.getenv("POSTGRES_DB", "crawler")
        self.postgres_user = os.getenv("POSTGRES_USER", "postgres")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD", "password")
        self.github_token = os.getenv("GITHUB_TOKEN")

def load_config():
    return Config()
