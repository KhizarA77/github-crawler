class CrawlerService:
    def __init__(self, github_client, postgres_repo):
        self.github_client = github_client
        self.postgres_repo = postgres_repo

    def run(self, limit=1000):
        total = 0
        end_cursor = None

        while total < limit:
            query = """
            query ($cursor: String) {
              search(query: "stars:>1000 sort:stars-desc", type: REPOSITORY, first: 100, after: $cursor) {
                edges {
                  node {
                    ... on Repository {
                      id
                      name
                      owner { login }
                      stargazerCount
                    }
                  }
                }
                pageInfo { endCursor hasNextPage }
              }
            }
            """

            data = self.github_client.query(query, {"cursor": end_cursor})
            repos = [
                (edge["node"]["id"], edge["node"]["name"], edge["node"]["owner"]["login"], edge["node"]["stargazerCount"])
                for edge in data["data"]["search"]["edges"]
            ]

            self.postgres_repo.bulk_upsert_repositories(repos)
            total += len(repos)

            print(f"Crawled {total} repositories so far...")

            end_cursor = data["data"]["search"]["pageInfo"]["endCursor"]
            if not data["data"]["search"]["pageInfo"]["hasNextPage"]:
                break
