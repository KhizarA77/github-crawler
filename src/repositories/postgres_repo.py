import psycopg2
from psycopg2.extras import execute_values

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

    def bulk_upsert_repositories(self, repos):
        """Efficient bulk UPSERT for large batches of repositories."""
        if not repos:
            return

        query = """
            INSERT INTO repositories (repo_id, name, owner, stars)
            VALUES %s
            ON CONFLICT (repo_id)
            DO UPDATE SET
                stars = EXCLUDED.stars,
                last_updated = CURRENT_TIMESTAMP;
        """

        try:
            with self.conn.cursor() as cur:
                execute_values(cur, query, repos, page_size=1000)
            self.conn.commit()
        except Exception as e:
            print(f"Error during bulk upsert: {e}")
            self.conn.rollback()

    def upsert_repository(self, repo_id, name, owner, stars):
        """Single-row UPSERT (for debugging or small updates)."""
        query = """
            INSERT INTO repositories (repo_id, name, owner, stars)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (repo_id)
            DO UPDATE SET
                stars = EXCLUDED.stars,
                last_updated = CURRENT_TIMESTAMP;
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (repo_id, name, owner, stars))
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting repository {repo_id}: {e}")
            self.conn.rollback()

    def close(self):
        """Cleanly close the database connection."""
        if self.conn:
            self.conn.close()
