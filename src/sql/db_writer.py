import mysql.connector
from prefect import get_run_logger, task
from prefect.tasks import exponential_backoff
from typing import List, Dict
from src.sql.db_config import get_db_connection


def episode_exists(cursor, audio_url: str) -> bool:
    """Checks whether an episode with the given audio URL already exists."""
    cursor.execute("SELECT 1 FROM episodes WHERE audio_url = %s LIMIT 1", (audio_url,))
    result = cursor.fetchone()
    exists = result is not None

    logger = get_run_logger()
    logger.info(f"Episode with audio_url={audio_url} exists? {exists}")

    return exists

def insert_episode(cursor, episode: dict) -> int:
    cursor.execute("""
        INSERT INTO episodes (
            episode_title, feed_title, description, summary,
            rss_url, audio_url, episode_link, published_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        episode.get("title"),
        episode.get("feed_title"),
        episode.get("description"),
        episode.get("summary"),
        episode.get("rss_url"),
        episode.get("audio_url"),
        episode.get("episode_link"),
        episode.get("published")
    ))
    return cursor.lastrowid

def insert_transcript_segments(cursor, episode_id: int, transcript_segments: List[Dict]):
    for segment in transcript_segments:
        cursor.execute("""
            INSERT INTO transcript_segments (
                episode_id, whisper_segment_id,
                segment_start, segment_end, segment_text
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            episode_id,
            segment.get("whisper_segment_id"),
            segment.get("start"),
            segment.get("end"),
            segment.get("text")
        ))

@task(
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=30),
    retry_jitter_factor=1,
)
def store_episode_data(episode: dict, transcript_segments: list[dict]):
    """Stores episode and transcript data in the database if not already present."""
    logger = get_run_logger()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if episode_exists(cursor, episode["audio_url"]):
            logger.info(f"Episode already exists: {episode['audio_url']}")
            return

        episode_id = insert_episode(cursor, episode)
        insert_transcript_segments(cursor, episode_id, transcript_segments)
        conn.commit()
        logger.info(f"Inserted episode {episode['title']} with {len(transcript_segments)} segments")
    except Exception as e:
        logger.error(f"Failed to insert episode: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
