# scripts/test_postgres_repo.py
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.infrastructure.postgres_repo import PostgresRepo

def main():
    repo = PostgresRepo()
    
    # Insert a new repo
    repo.upsert_repository(
        repo_id=12345,
        name="octocat/Hello-World",
        owner="octocat",
        stars=42
    )
    print("Inserted first repo")

    # Update the star count (to simulate change)
    repo.upsert_repository(
        repo_id=12345,
        name="octocat/Hello-World",
        owner="octocat",
        stars=100
    )
    print("Updated star count")

    repo.close()

if __name__ == "__main__":
    main()
