USE podcasts;

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