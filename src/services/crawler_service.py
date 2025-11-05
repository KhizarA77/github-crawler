import time

star_ranges = [
    "stars:>50000",
    "stars:10000..50000",
    "stars:5000..9999",
    "stars:1000..4999",
    "stars:500..999",
    "stars:100..499",
    "stars:50..99",
    "stars:10..49",
    "stars:1..9"
]
class CrawlerService:
    def __init__(self, github_client, postgres_repo):
        self.github_client = github_client
        self.postgres_repo = postgres_repo

    def run(self, limit=100000):
      total = 0
      for range_query in star_ranges:
          end_cursor = None
          while total < limit:
              query = """
              query ($cursor: String, $searchQuery: String!) {
                search(query: $searchQuery, type: REPOSITORY, first: 100, after: $cursor) {
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

              data = self.github_client.query(query, {
                  "cursor": end_cursor,
                  "searchQuery": f"{range_query} sort:stars-desc"
              })

              repos = [
                  (
                      edge["node"]["id"],
                      edge["node"]["name"],
                      edge["node"]["owner"]["login"],
                      edge["node"]["stargazerCount"]
                  )
                  for edge in data["data"]["search"]["edges"]
              ]

              self.postgres_repo.bulk_upsert_repositories(repos)
              total += len(repos)

              print(f"Crawled {total} repositories so far ({range_query})")

              end_cursor = data["data"]["search"]["pageInfo"]["endCursor"]
              if not data["data"]["search"]["pageInfo"]["hasNextPage"]:
                  break

          if total >= limit:
              break

      print(f"Crawl complete! Total repositories saved: {total}")

