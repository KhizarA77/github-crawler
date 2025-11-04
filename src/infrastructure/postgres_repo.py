import psycopg2
from psycopg2.extras import execute_batch

class PostgresRepo:
    def __init__(self, config):
        self.conn = psycopg2.connect(
            host=config.postgres_host,
            port=config.postgres_port,
            database=config.postgres_db,
            user=config.postgres_user,
            password=config.postgres_password,
        )
        self.conn.autocommit = False

    def upsert_repository(self, repo_id, name, owner, stars):
        query = """
            INSERT INTO repositories (repo_id, name, owner, stars)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (repo_id)
            DO UPDATE SET
                stars = EXCLUDED.stars,
                last_updated = CURRENT_TIMESTAMP;
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (repo_id, name, owner, stars))
        self.conn.commit()

    def bulk_upsert_repositories(self, repos):
        query = """
            INSERT INTO repositories (repo_id, name, owner, stars)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (repo_id)
            DO UPDATE SET
                stars = EXCLUDED.stars,
                last_updated = CURRENT_TIMESTAMP;
        """
        with self.conn.cursor() as cur:
            execute_batch(cur, query, repos, page_size=100)
        self.conn.commit()

    def close(self):
        self.conn.close()
