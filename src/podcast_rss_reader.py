import feedparser
import time
from datetime import datetime
from typing import Dict, List, Optional, cast

class PodcastRSSFeedReader:
    """Parses a podcast RSS feed and extracts episode metadata.

    Attributes:
        rss_url (str): The URL of the RSS feed.
        feed (feedparser.FeedParserDict): Parsed feed data.
    """

    def __init__(self, rss_url):
        """Initializes the PodcastRSSFeedReader with a given RSS URL.

        Args:
            rss_url (str): The URL to the podcast RSS feed.
        """
        self.rss_url = rss_url
        self.feed = feedparser.parse(rss_url)


    def get_episodes(self, filter_by_year:Optional[int]) -> List[Dict]:
        """Extracts episode metadata from the RSS feed, optionally filtered by year.

        Args:
            filter_by_year (int, optional): Only include episodes published in this year. Defaults to 2024.

        Returns:
            list: A list of dictionaries, each containing:
                - rss_url (str): the url for the rss feed
                - title (str): Title of the episode.
                - audio_url (str): Direct URL to the episode's audio file.
                - summary (str): Short summary of the episode.
                - published (datetime): Publication timestamp as a datetime object.
                - description (str): HTML description (if available).
                - episode_link (str): Webpage link for the episode.
                - feed_title (str): Title of the podcast feed.
        """
        episodes = []
        for entry in self.feed.entries:
            published_parsed = getattr(entry, "published_parsed", None)
            pub_year = published_parsed.tm_year if published_parsed else None # get year only for comparison

            if filter_by_year is not None and pub_year != filter_by_year:
                continue

            audio_url = entry.enclosures[0].href if entry.enclosures else "unknown audio_url"
            published = datetime(*published_parsed[:6]) if published_parsed else datetime(1900, 1, 1)

            episodes.append({
                "rss_url": self.rss_url,
                "title": getattr(entry, "title", "unknown title"),
                "audio_url": audio_url,
                "summary": getattr(entry, "summary", "no summary"),
                "published": published,
                "description": getattr(entry, "description", "no description"),
                "episode_link": getattr(entry, "link", "no episode link"),
                "feed_title": self.feed.feed.get("title", "unknown title")  # type: ignore
            })
        return episodes


def main():
    rss_url = "https://feeds.megaphone.fm/VMP7924981569"
    reader = PodcastRSSFeedReader(rss_url)
    episodes = reader.get_episodes(filter_by_year=2024)
    for ep in episodes:
        print(f"{ep['published']} - {ep['title']}\n{ep['url']}\n")

if __name__ == "__main__":
    main()