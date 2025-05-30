CREATE TABLE IF NOT EXISTS episodes (
    episode_id INT AUTO_INCREMENT PRIMARY KEY,
    rss_url TEXT,
    feed_title VARCHAR(255),
    episode_title VARCHAR(255),
    audio_url TEXT,
    published_at DATETIME,
    description TEXT,
    summary TEXT,
    episode_link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
