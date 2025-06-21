import os
import logging
import requests
import feedparser

from typing import Tuple
from datetime import datetime
from models.downloaders.downloader import Downloader

logger = logging.getLogger(__name__)

DEFAULT_FILE_EXT = ".mp3"
DEFAULT_CHUNK_SIZE = 8192  # 8 KB
DEFAULT_DOWNLOADS_DIR = "downloads"


class RSS_Feed_Downloader(Downloader):
    """
    A class for downloading podcast episodes from an RSS feed.

    Attributes:
        config (dict): Configuration settings including download directory, file extension, and chunk size.
        verbose (bool): Enables detailed logging output when True.
    """

    def __init__(self, config: dict):
        """
        Initializes the RSS_Feed_Downloader with the given configuration.

        Args:
            config (dict): Configuration dictionary.
                - 'verbose' (bool): Enables verbose logging.
                - 'downloads_dir' (str): Directory to store downloaded episodes (default: "downloads").
                - 'file_ext' (str): File extension for saved audio (default: ".mp3").
                - 'chunk_size' (int): Size of download chunks in bytes (default: 8192).
        """
        self.config = config
        self.verbose = config.get("verbose", False)

    def download_episode(
        self, source_url: str, episode_name: str | None
    ) -> Tuple[str, dict]:
        """
        Downloads a podcast episode from the specified RSS feed.

        Args:
            source_url (str): URL of the RSS feed.
            episode_name (str | None): Name of the episode to download. If None, the latest episode will be selected.

        Returns:
            Tuple[str, dict]: A tuple containing:
                - file_path (str): Local path to the downloaded episode.
                - metadata (dict): Episode metadata including title, thumbnail, duration, release date, id, and channel name.
        Raises:
            ValueError: If the episode is not found or does not contain a downloadable audio file.
            requests.HTTPError: If the download fails due to a bad HTTP response.
        """
        entry, channel_name = self._get_episode_entry(source_url, episode_name)

        if not entry:
            raise ValueError("Episode not found. Please check the episode name.")

        if "enclosures" not in entry and not entry.enclosures:
            raise ValueError("No audio enclosure available.")

        mp3_url = entry.enclosures[0].href
        episode_id = mp3_url.split("/")[-1].split(".")[0]

        output_dir = os.path.join(
            os.getcwd(),
            self.config.get("downloads_dir", DEFAULT_DOWNLOADS_DIR),
            episode_id,
        )
        os.makedirs(os.path.join(output_dir, episode_id), exist_ok=True)
        file_path = os.path.join(
            output_dir,
            episode_id,
            episode_id + self.config.get("file_ext", DEFAULT_DOWNLOADS_DIR),
        )

        metadata = self._get_metadata(entry)
        metadata["video_id"] = episode_id
        metadata["channel"] = channel_name

        if self.verbose and os.path.exists(file_path):
            logger.info("Episode already downloaded.")
            return file_path, metadata

        response = requests.get(mp3_url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(
                chunk_size=self.config.get("chunk_size", DEFAULT_CHUNK_SIZE)
            ):
                file.write(chunk)

        if self.verbose:
            logger.info("Successfully downloaded episode.")

        return file_path, metadata

    def _get_episode_entry(
        self, source_url: str, episode_name: str
    ) -> Tuple[dict, str] | Tuple[None, None]:
        """
        Retrieves an episode entry from the RSS feed by matching the title.

        Args:
            source_url (str): The URL of the RSS feed.
            episode_name (str): The title of the desired episode.

        Returns:
            Tuple[dict, str] | Tuple[None, None]: A tuple containing:
                - entry (dict): The RSS entry of the episode.
                - channel_name (str): The title of the podcast channel.
            Returns (None, None) if the episode is not found.
        """
        feed = feedparser.parse(source_url)
        channel_name = feed.get("channel", {}).get("title", "")
        for entry in feed.entries:
            if episode_name.lower() == entry.title.lower():
                return entry, channel_name
        return None, None

    def _get_metadata(self, entry: dict) -> dict:
        """
        Extracts metadata from a feed entry.

        Args:
            entry (dict): An RSS feed entry object.

        Returns:
            dict: Metadata dictionary with the following keys:
                - 'title' (str): Title of the episode.
                - 'thumbnail' (str | None): URL to the episode image, if available.
                - 'duration_string' (str | None): Duration in hh:mm:ss or mm:ss format.
                - 'release_date' (str): Release date in "YYYY-MM-DD" format.
        """
        raw_duration = entry.get("itunes_duration")
        if raw_duration and raw_duration.isdigit():
            duration_string = self._format_duration(int(raw_duration))
        else:
            duration_string = raw_duration

        published_parsed = entry.get("published_parsed")
        dt = datetime(*published_parsed[:6])
        date_str = dt.strftime("%Y-%m-%d")

        return {
            "title": entry.get("title", ""),
            "thumbnail": entry.get("image", {}).get("href"),
            "duration_string": duration_string,
            "release_date": date_str,
        }

    def _format_duration(self, seconds: int) -> str:
        """
        Converts a duration in seconds to a formatted string.

        Args:
            seconds (int): The duration in seconds.

        Returns:
            str: Duration formatted as "HH:MM:SS" or "MM:SS" if under an hour.
        """
        seconds = int(seconds)
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{secs:02}"
        else:
            return f"{minutes}:{secs:02}"
