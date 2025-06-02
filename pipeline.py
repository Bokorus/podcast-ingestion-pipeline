from prefect import flow, task, get_run_logger
from prefect.tasks import exponential_backoff
import csv
from src.podcast_rss_reader import PodcastRSSFeedReader
from src.audio2text import Audio2Text
from src.sql.db_config import get_db_connection
from src.sql.db_writer import insert_episode, insert_transcript_segments, episode_exists

@task
def read_rss_csv(path: str) -> list[str]:
    """ Reads RSS feed URLs from a CSV file.

    Args:
        path (str): Path to the CSV file containing RSS feed URLs.

    Returns:
        list[str]: A list of RSS feed URLs extracted from the file.
    """
    logger = get_run_logger()
    logger.info(f"Reading RSS URLs from {path}")
    rss_urls = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rss_urls.append(row['rss_url'])
    logger.info(f"Found {len(rss_urls)} RSS URLs")
    return rss_urls

@task
def fetch_episodes(rss_url: str, year: int) -> list[dict]:
    """ Fetches podcast episodes from an RSS feed, optionally filtered by year.

    Args:
        rss_url (str): The RSS feed URL.
        year (int): The publication year to filter episodes by.

    Returns:
        list[dict]: A list of episode metadata dictionaries.
    """
    logger = get_run_logger()
    logger.info(f"Fetching episodes for RSS URL: {rss_url} and year: {year}")
    reader = PodcastRSSFeedReader(rss_url)
    episodes = reader.get_episodes(filter_by_year=year)
    logger.info(f"Fetched {len(episodes)} episodes for RSS URL: {rss_url}")
    return episodes

@task
def download_audio(url: str) -> str:
    """ Downloads the audio file from the given URL and returns its local file path.

    Args:
        url (str): Direct URL to the podcast episode's audio file.

    Returns:
        str: The local path to the downloaded audio file.
    """
    logger = get_run_logger()
    logger.info(f"Downloading audio for URL: {url}")
    transcriber = Audio2Text()
    audio_filename = transcriber.get_audio_filename_from_url(url)
    audio_path = transcriber.download_audio(url, audio_filename)
    logger.info(f"Downloaded audio to {audio_path}")
    return audio_path

@task
def transcribe_audio(audio_path: str) -> list[dict]:
    """ Transcribes the audio file into segments using Whisper.

    Args:
        audio_path (str): Path to the downloaded audio file.

    Returns:
        list[dict]: A list of transcription segments, each represented as a dictionary.
    """
    logger = get_run_logger()
    logger.info(f"Transcribing audio file: {audio_path}")
    transcriber = Audio2Text()
    segments = transcriber.transcribe(audio_path)
    logger.info(f"Transcribed {len(segments)} segments from audio file: {audio_path}")
    return segments

@task
def log_episode_transcript(episode: dict, transcript_segments: list[dict]):
    """ Logs episode title and a preview of its first transcript segment.

    Args:
        episode (dict): Metadata dictionary for the episode.
        transcript_segments (list[dict]): List of transcribed segments for the episode.
    """
    logger = get_run_logger()
    logger.info(f"Episode: {episode['title']}")
    if transcript_segments:
        logger.info(f"First segment (first 100 chars): {transcript_segments[0]['text'][:100]}")
    else:
        logger.info("No transcript segments available.")

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

@flow
def audio_pipeline(csv_path: str = 'rss_feeds.csv'):
    """Main pipeline flow to process podcast RSS feeds.

    Args:
        csv_path (str): Path to the CSV file containing RSS feed URLs. Defaults to 'rss_feeds.csv'.
    """
    logger = get_run_logger()
    logger.info("Starting audio_pipeline flow")
    rss_urls = read_rss_csv(csv_path)

    for rss_url in rss_urls:
        episodes = fetch_episodes(rss_url, 2024)
        for episode in episodes:
            conn = get_db_connection()
            cursor = conn.cursor()
            if episode_exists(cursor, episode["audio_url"]):
                logger.info(f"Skipping existing episode: {episode['audio_url']}")
                cursor.close()
                conn.close()
                continue
            cursor.close()
            conn.close()

            audio_path = download_audio(episode['audio_url'])
            transcript_segments = transcribe_audio(audio_path)
            log_episode_transcript(episode, transcript_segments)
            store_episode_data(episode, transcript_segments)
    logger.info("Completed audio_pipeline flow")

if __name__ == "__main__":
    audio_pipeline()
