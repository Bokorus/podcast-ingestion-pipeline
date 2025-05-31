CREATE TABLE IF NOT EXISTS episodes (
    episode_id INT AUTO_INCREMENT PRIMARY KEY,
    episode_title TEXT,
    feed_title TEXT,
    description TEXT,
    summary TEXT,
    rss_url TEXT,
    audio_url TEXT,
    episode_link TEXT,
    published_at DATETIME
);
