# 📟 Podcast Ingestion & Transcription Pipeline

This repository contains a pipeline for scraping podcast episodes from RSS feeds, transcribing audio with Whisper, and storing metadata and transcript segments in a cloud-hosted MySQL database for analysis.

## 🚀 Features

* Downloads podcast episodes from RSS feeds (2024 only)
* Transcribes audio using [OpenAI Whisper](https://github.com/openai/whisper)
* Segments transcripts into utterances
* Stores metadata and segments in MySQL (AWS RDS)
* Includes election-related content query

## 💠 Requirements

* Python 3.11+
* `ffmpeg` installed and on your PATH
* `whisper`, `mysql-connector-python`, `requests`, `python-dotenv`, `prefect`, etc.

Install dependencies:

```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```bash
.
├── data/                  # Temporary audio files
├── src/
│   ├── rss_reader.py      # Parses RSS feeds & downloads episodes
│   ├── audio2text.py      # Downloads & transcribes audio
│   ├── db_writer.py       # Inserts metadata & segments into MySQL
│   └── pipeline.py        # Orchestrates tasks via Prefect
├── sql/
│   ├── create_tables.sql  # Schema for `episodes` and `transcript_segments`
│   └── election_query.sql # Election-related SQL query
├── .env                   # Environment variables (MySQL credentials)
├── rss_feeds.csv          # Provided RSS feed list
└── README.md
```

## 🔧 Setup

1. **Create `.env` file**

```bash
cp .env.template .env
```

Edit it to match your database connection:

```dotenv
DB_HOST=your-db-host.rds.amazonaws.com
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=podcasts
```

2. **Run the pipeline**

```bash
python -m src.pipeline
```

This will:

* Read RSS feeds
* Download 2024 episodes
* Transcribe audio
* Insert data into MySQL

## 📓 SQL Query for Election Mentions

```sql
-- See: sql/election_query.sql
SELECT e.episode_title, e.feed_title
FROM episodes e
JOIN transcript_segments t ON e.episode_id = t.episode_id
WHERE LOWER(t.segment_text) REGEXP '\\b(trump|biden)\\b'
  AND e.published_at BETWEEN '2024-10-22' AND '2024-11-19';
```

## 📝 Notes

* Database must be cloud-accessible (e.g., AWS RDS)
* Ensure your IP is whitelisted in the RDS security group
* Transcript segments are utterance-level (not sentence-based)

<!-- ## 📜 License

MIT -->
