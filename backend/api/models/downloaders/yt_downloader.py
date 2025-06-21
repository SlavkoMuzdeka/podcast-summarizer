import os
import json
import logging

from typing import Tuple
from yt_dlp import YoutubeDL
from models.downloaders.downloader import Downloader

logger = logging.getLogger(__name__)

DEFAULT_FILE_EXT = ".mp3"
DEFAULT_DOWNLOADS_DIR = "downloads"
DEFAULT_METADATA_EXT = ".info.json"


class YT_Downloader(Downloader):
    """
    A class for downloading YouTube videos as MP3 audio files and retrieving their metadata.

    Inherits from:
        Downloader

    Attributes:
        config (dict): Configuration settings for downloading and verbosity.
        verbose (bool): Enables detailed logging output when True.
        source_url (str): The sanitized YouTube URL (without extra parameters).
        video_id (str): Unique YouTube video identifier extracted from the URL.
    """

    def __init__(self, config: dict):
        """
        Initializes the YouTube_Downloader with a configuration dictionary.

        Args:
            config (dict): Configuration settings including:
                - 'verbose' (bool): Enable verbose logging (default: False).
                - 'downloads_dir' (str): Directory to store downloads (default: "downloads").
                - 'file_ext' (str): Extension for audio file (default: ".mp3").
                - 'metadata_ext' (str): Extension for metadata file (default: ".info.json").
        """
        self.config = config
        self.verbose = self.config.get("verbose", False)

    def download_episode(
        self, source_url: str, episode_name: str | None
    ) -> Tuple[str, dict]:
        """
        Downloads a YouTube video as an MP3 file and retrieves its metadata.

        Args:
            source_url (str): The full YouTube video URL.
            episode_name (str | None): Unused parameter included for compatibility with the base class.

        Returns:
            Tuple[str, dict]: A tuple containing:
                - mp3_path (str): Path to the downloaded MP3 file.
                - metadata (dict): Metadata dictionary enriched with the video ID.

        Raises:
            Exception: If downloading fails or metadata cannot be read.
        """
        self.source_url = source_url.split("&")[0]
        self.video_id = self.source_url.split("=")[-1]

        mp3_path = self._download_mp3()
        metadata = self._download_metadata()
        metadata["video_id"] = self.video_id

        return mp3_path, metadata

    def _download_mp3(self) -> str:
        """
        Downloads the YouTube video as an MP3 audio file.

        Returns:
            str: Path to the downloaded MP3 file.

        Raises:
            Exception: If the download fails.
        """
        return self._download_file(
            extension=self.config.get("file_ext", DEFAULT_FILE_EXT), audio_only=True
        )

    def _download_metadata(self) -> dict:
        """
        Downloads the metadata for the YouTube video and returns its contents.

        Returns:
            dict: A dictionary containing the video's metadata.

        Raises:
            Exception: If reading the metadata file fails.
        """
        metadata_path = self._download_file(
            extension=self.config.get("metadata_ext", DEFAULT_METADATA_EXT)
        )

        try:
            with open(metadata_path, "r", encoding="utf8") as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Failed to read metadata file: {e}")
            return {}

    def _download_file(self, extension: str, audio_only: bool = False) -> str:
        """
        Downloads either the MP3 audio or metadata JSON file.

        Args:
            extension (str): File extension (e.g., ".mp3" or ".info.json").
            audio_only (bool): Whether to download only the audio (MP3). Defaults to False.

        Returns:
            str: Path to the downloaded file.

        Raises:
            Exception: If the download fails.
        """
        output_path = os.path.join(
            os.getcwd(),
            self.config.get("downloads_dir", DEFAULT_DOWNLOADS_DIR),
            self.video_id,
            f"{self.video_id}{extension}",
        )

        if self.verbose:
            if os.path.exists(output_path):
                logger.info(f"File already exists ({extension}).")
                return output_path

        with YoutubeDL(
            self._get_ydl_opts(
                self.config.get("downloads_dir", DEFAULT_DOWNLOADS_DIR), audio_only
            )
        ) as ydl:
            try:
                ydl.download([self.source_url])
            except Exception as e:
                logger.error(f"Failed to download {extension}: {e}")
                raise

        if self.verbose:
            logger.info(f"Successfully downloaded file ({extension}).")

        return output_path

    def _get_ydl_opts(self, output_dir: str, audio_only: bool = False) -> dict:
        """
        Prepares yt-dlp configuration options based on the desired download type.

        Args:
            output_dir (str): Directory where the file will be saved.
            audio_only (bool): If True, only audio will be downloaded and converted to MP3.

        Returns:
            dict: Configuration dictionary to be passed to YoutubeDL.
        """
        opts = {
            "outtmpl": os.path.join(output_dir, "%(id)s", "%(id)s.%(ext)s"),
        }

        if audio_only:
            opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            )
        else:
            opts.update(
                {
                    "skip_download": True,
                    "writeinfojson": True,
                }
            )
        return opts
