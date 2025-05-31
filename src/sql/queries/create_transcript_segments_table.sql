CREATE TABLE IF NOT EXISTS transcript_segments (
    segment_id INT AUTO_INCREMENT PRIMARY KEY,
    episode_id INT,
    whisper_segment_id INT,
    segment_start FLOAT,
    segment_end FLOAT,
    segment_text TEXT,
    FOREIGN KEY (episode_id) REFERENCES episodes(episode_id) ON DELETE CASCADE,
    FULLTEXT (segment_text)
);