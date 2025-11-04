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

    def query(self, query: str, variables: dict = None):
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v4+json"
        }


        for attempt in range(3):
            response = requests.post(self.url, json={"query": query, "variables": variables}, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    print("Error from GitHub API: ", data["errors"])
                return data
            elif response.status_code == 403:
                reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                sleep_for = max(0, reset_time - time.time())
                print(f"Rate limit hit. Sleeping for {sleep_for:.0f}s...")
                time.sleep(sleep_for)
            else:
                print(f"Request failed with {response.status_code}: {response.text}")
                time.sleep(2)

        raise Exception("Failed to fetch data from GitHub API after multiple retries.")
