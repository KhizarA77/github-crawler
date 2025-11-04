# scripts/test_github_client.py
from src.repositories.github_client import GitHubClient

def main():
    client = GitHubClient()
    query = """
    {
      viewer {
        login
      }
      rateLimit {
        limit
        remaining
        resetAt
      }
    }
    """
    data = client.query(query)
    print("API test successful.")
    print("Authenticated as:", data["data"]["viewer"]["login"])
    print("Rate limit info:", data["data"]["rateLimit"])

if __name__ == "__main__":
    main()
