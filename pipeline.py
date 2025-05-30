from prefect import flow, task, get_run_logger
import csv
from src.podcast_rss_reader import PodcastRSSFeedReader
from src.audio2text import Audio2Text

@task
def read_rss_csv(path: str) -> list[str]:
    rss_urls = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rss_urls.append(row['rss_url'])
    return rss_urls

@task
def fetch_episodes(rss_url: str, year: int) -> list[dict]:
    reader = PodcastRSSFeedReader(rss_url)
    return reader.get_episodes(filter_by_year=year)

@task
def download_audio(url: str) -> str:
    transcriber = Audio2Text()
    return transcriber.download_audio(url)

@task
def transcribe_audio(audio_path: str) -> str:
    transcriber = Audio2Text()
    return transcriber.transcribe(audio_path)

@task
def log_episode_transcript(episode: dict, transcript: str):
    logger = get_run_logger()
    logger.info(f"Episode: {episode['title']}")
    logger.info(f"Transcript (first 100 chars): {transcript[:100]}")

@flow
def audio_pipeline(csv_path: str = 'rss_feeds.csv'):
    rss_urls = read_rss_csv(csv_path)

    for rss_url in rss_urls:
        episodes = fetch_episodes(rss_url, 2024)
        for episode in episodes:
            audio_path = download_audio(episode['url'])
            transcript = transcribe_audio(audio_path)
            log_episode_transcript(episode, transcript)
            # TODO: Store to database or serialize to disk

if __name__ == "__main__":
    audio_pipeline()
