
# 🕸️ GitHub Crawler

This project is a **GitHub Crawler** that uses the **GitHub GraphQL API** to collect and store metadata about public repositories — specifically, repository names, owners, and star counts — in a **PostgreSQL database**.  
It is designed for efficient, continuous crawling and adheres to clean software engineering principles.

---

## 🚀 Features

- Fetches data for **100,000 public GitHub repositories**
- Stores data efficiently in **PostgreSQL**
- Automatically sets up schema via **GitHub Actions**
- Respects **API rate limits** and includes retry mechanisms
- Can run continuously (daily) to update repository data
- Fully automated **CI/CD pipeline** using **GitHub Actions**
- Works entirely with the **default `GITHUB_TOKEN`**
- Extensible schema for collecting more metadata in the future

---

## 🧱 Project Structure

```
github-crawler/
│
├── src/
│   ├── main.py              # Crawler logic using GitHub GraphQL API
│   ├── config.py            # Loads configuration and credentials
│   ├── services/
|     ├── crawler_service.py
|   ├── repositories/
|     ├── github_client.py
|     ├── postgres_repo.py
├── scripts/
│   ├── setup_postgres.py    # Creates the PostgreSQL schema
│   ├── crawl_stars.py
|   ├── test_connection.py
|   ├── test_github_client.py
├── requirements.txt         
├── .github/workflows/crawler.yml # GitHub Actions CI pipeline
└── README.md                
```

---

## 🗃️ Database Schema

```sql
CREATE TABLE IF NOT EXISTS repositories (
    repo_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    owner TEXT NOT NULL,
    stars INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Why This Schema?
- **Primary key:** `repo_id` ensures each repo is unique.
- **Efficient updates:** Uses `ON CONFLICT (repo_id) DO UPDATE` to refresh data without duplication.
- **Extensible:** Future tables (e.g. issues, PRs, comments) can reference `repo_id` as a foreign key.

---

## ⚙️ GitHub Actions CI/CD Pipeline

This repository includes a complete CI pipeline that:

1. Spins up a **PostgreSQL service container**
2. Installs dependencies and sets up a virtual environment
3. Creates the database schema (`setup_postgres.py`)
4. Runs the GitHub Crawler (`src/main.py`)
5. Exports crawled data to `repositories.csv`
6. Uploads the CSV as an **artifact** for easy download

---

### Example Workflow Snippet

```yaml
- name: Export crawled data
  run: |
    source venv/bin/activate
    python -c "
import psycopg2, csv;
conn=psycopg2.connect(host='localhost', port=5432, dbname='crawler', user='user', password='password');
cur=conn.cursor();
cur.execute('SELECT * FROM repositories');
rows=cur.fetchall();
with open('repositories.csv','w',newline='') as f:
    writer=csv.writer(f);
    writer.writerow(['repo_id','name','owner','stars','last_updated']);
    writer.writerows(rows);
conn.close();
"

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: crawled-data
    path: repositories.csv
```

---

## 🧩 Design and Architecture

### Clean Architecture Principles
- **Separation of concerns:** Each module has a single responsibility.
- **Immutability where possible:** Data transformations are side-effect-free.
- **Anti-corruption layer:** The GitHub API is abstracted from the core logic.
- **Extensibility:** Schema and code can evolve for future metadata collection.

### Example: Extending Schema
To add pull requests or issues, simply define related tables:
```sql
CREATE TABLE pull_requests (
    pr_id TEXT PRIMARY KEY,
    repo_id TEXT REFERENCES repositories(repo_id),
    title TEXT,
    comments_count INTEGER,
    updated_at TIMESTAMP
);
```

---

## 📈 Scaling to 500 Million Repositories

If scaling from 100K → 500M repositories, we would:

1. **Distribute crawling** across multiple workers and GitHub tokens.  
2. **Shard the database** by `repo_id` ranges or hash partitioning.  
3. **Use asynchronous crawling** (e.g., asyncio + aiohttp) to maximize throughput.  
4. **Stream inserts** into the DB to reduce transaction overhead.  
5. **Introduce caching and rate-limit aware scheduling.**  
6. **Move to data warehouses** (e.g., BigQuery, Redshift) for large-scale analytics.  

---

## 🧠 Usage

Run locally:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export GITHUB_TOKEN=your_personal_token
python scripts/setup_postgres.py
python -m src.main
```

Run via GitHub Actions:
- Simply **push to the `main` branch** — the CI pipeline runs automatically.

---

## ✅ Submission Checklist

| Requirement | Status |
|--------------|---------|
| PostgreSQL container | ✅ |
| Dependency setup | ✅ |
| Schema setup step | ✅ |
| Crawl 100k repos | ✅ |
| Dump + artifact upload | ✅ |
| Uses default `GITHUB_TOKEN` | ✅ |
| Schema flexibility | ✅ |
| Clean architecture | ✅ |
| Scaling plan included | ✅ |

---

## 🧾 License
MIT License © 2025
