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
├── src/
│   ├── rss_reader.py        # Parses RSS feeds & downloads episodes
│   ├── audio2text.py        # Downloads & transcribes audio
│   ├── pipeline.py          # Orchestrates tasks via Prefect
├── sql/
│   ├── db_config.py         # Database connection config
│   ├── db_writer.py         # Inserts metadata & segments into MySQL
│   ├── create_db_tables.py  # Creates database tables
│   └── queries/
│       ├── create_episodes_table.sql
│       ├── create_transcript_segments_table.sql
│       └── presidential-candidate-query.sql
├── .env                     # Environment variables (MySQL credentials)
├── rss_feeds.csv            # RSS feed list for ingestion
└── README.md
```

## 🔧 Setup

1. **Create `.env` file**

```bash
cp .env.template .env
```

Edit it to match your database connection:

```dotenv
DB_HOST=<your-rds-endpoint>
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
SELECT DISTINCT e.episode_id,
       e.episode_title,
       e.feed_title AS podcast_title,
       e.published_at,
       t.segment_text
FROM episodes e
JOIN transcript_segments t
  ON e.episode_id = t.episode_id
WHERE DATE(e.published_at) BETWEEN '2024-10-22' AND '2024-11-19'
  AND (
    LOWER(t.segment_text) REGEXP '\\btrump\\b' OR
    LOWER(t.segment_text) REGEXP '\\bbiden\\b'
)
ORDER BY e.published_at ASC;
```

## 📝 Notes

* Database must be cloud-accessible (e.g., AWS RDS)
* Ensure your IP is whitelisted in the RDS security group
* Transcript segments are utterance-level (not sentence-based)

<!-- ## 📜 License

MIT -->
