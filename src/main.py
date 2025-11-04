from src.config import load_config
from src.infrastructure.postgres_repo import PostgresRepo
from src.infrastructure.github_client import GitHubClient
from src.services.crawler_service import CrawlerService

def main():
    print("Starting GitHub crawler")

    config = load_config()

    github_client = GitHubClient(config.github_token)
    postgres_repo = PostgresRepo(config)
    crawler_service = CrawlerService(github_client, postgres_repo)

    # Run crawler
    crawler_service.run()

    # Clean up
    postgres_repo.close()
    print("Crawl complete!")

if __name__ == "__main__":
    main()
