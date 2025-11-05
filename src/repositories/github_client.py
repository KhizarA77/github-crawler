import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class GitHubClient:
    def __init__(self, token=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN missing")

        self.url = "https://api.github.com/graphql"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v4+json"
        })

    def query(self, query: str, variables: dict = None):
        """Performs a GitHub GraphQL query with retry, backoff, and rate-limit handling."""
        for attempt in range(3):
            try:
                response = self.session.post(
                    self.url,
                    json={"query": query, "variables": variables or {}},
                    timeout=20
                )

                # Handle rate limits
                if response.status_code == 403:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                    sleep_for = max(0, reset_time - time.time()) + 5
                    print(f"Rate limit hit. Sleeping for {sleep_for:.0f}s...")
                    time.sleep(sleep_for)
                    continue

                if response.status_code != 200:
                    print(f"Request failed ({response.status_code}): {response.text}")
                    time.sleep(3)
                    continue

                data = response.json()

                if "errors" in data:
                    print(f"GraphQL error: {data['errors']}")
                    time.sleep(5)
                    continue

                return data

            except requests.RequestException as e:
                print(f"Request error: {e}. Retrying...")
