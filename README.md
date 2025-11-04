# init
docker run --name github-crawler-db  -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=crawler -p 5432:5432 -d postgres:latest