import time
from src.infrastructure.github_client import GitHubClient
from src.infrastructure.postgres_repo import PostgresRepo

REPO_QUERY = """
query ($cursor: String) {
  search(query: "stars:>0 sort:stars-desc", type: REPOSITORY, first: 100, after: $cursor) {
    edges {
      node {
        ... on Repository {
          id
          name
          owner {
            login
          }
          stargazerCount
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""

def crawl_repositories(limit=100000):
    client = GitHubClient()
    repo = PostgresRepo()

    cursor = None
    total = 0
    print("🚀 Starting crawl...")

    while total < limit:
        data = client.query(REPO_QUERY, {"cursor": cursor})
        edges = data["data"]["search"]["edges"]

        if not edges:
            print("No more repos found.")
            break

        repos = [
            (
                e["node"]["id"],
                e["node"]["name"],
                e["node"]["owner"]["login"],
                e["node"]["stargazerCount"],
            )
            for e in edges
        ]

        repo.bulk_upsert_repositories(repos)

        total += len(repos)
        print(f"✅ Crawled {total} repositories so far...")

        page_info = data["data"]["search"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break

        cursor = page_info["endCursor"]
        time.sleep(1) 

    repo.close()
    print(f"🎉 Done! Total crawled: {total}")

if __name__ == "__main__":
    crawl_repositories()
