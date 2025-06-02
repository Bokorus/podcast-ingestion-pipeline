from prefect import flow
from pipeline import (
    read_rss_csv,
    fetch_episodes,
    download_audio,
    transcribe_audio,
)
from src.sql.db_config import get_db_connection
from src.sql.db_writer import insert_episode, insert_transcript_segments

@flow
def test_pipeline_tasks():
    # 1. test reading rss urls
    rss_path = "rss_feeds.csv" 
    rss_urls = read_rss_csv.fn(rss_path)
    print(f"\n[✓] RSS URLs read: {rss_urls}\n")

    if not rss_urls:
        print("✗ No RSS URLs found. Exiting.")
        return

    # 2. test fetching episodes
    episodes = fetch_episodes.fn(rss_urls[0], 2024)
    print(f"[✓] Fetched {len(episodes)} episodes\n")

    if not episodes:
        print("✗ No episodes found. Exiting.")
        return

    # 3. test downloading audio and transcription
    audio_path = download_audio.fn(episodes[0]["audio_url"])
    print(f"[✓] Audio downloaded to: {audio_path}\n")

    segments = transcribe_audio.fn(audio_path)
    print(f"[✓] Transcribed {len(segments)} segments\n")
    print("First segment preview:")
    print(segments[0] if segments else "✗ No segments")

@flow
def test_db_insert():
    mock_episode = {
        "title": "Test Episode",
        "feed_title": "Test Podcast",
        "description": "Test description",
        "summary": "Short summary",
        "rss_url": "https://example.com/rss",
        "audio_url": "https://example.com/audio.mp3",
        "episode_link": "https://example.com/ep1",
        "published": "2024-01-01 00:00:00"
    }

    mock_segments = [
        {
            "whisper_segment_id": 0,
            "start": 0.0,
            "end": 2.5,
            "text": "Welcome to the show."
        },
        {
            "whisper_segment_id": 1,
            "start": 2.5,
            "end": 5.0,
            "text": "Here's what we're covering."
        }
    ]

    conn = get_db_connection()
    cursor = conn.cursor()
    episode_id = insert_episode(cursor, mock_episode)
    insert_transcript_segments(cursor, episode_id, mock_segments)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"[✓] Inserted test episode with ID: {episode_id}")

if __name__ == "__main__":
    # test_pipeline_tasks()
    test_db_insert()