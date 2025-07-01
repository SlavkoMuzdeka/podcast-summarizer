import os
import json
import shutil
import logging

from typing import Tuple
from yt_dlp import YoutubeDL

from models.downloaders.downloader import Downloader

logger = logging.getLogger(__name__)

DEFAULT_FILE_EXT = ".mp3"
DEFAULT_METADATA_EXT = ".info.json"


class YT_Downloader(Downloader):
    def __init__(self, config: dict):
        self.config = config
        self.verbose = config.get("verbose", False)
        self.on_vercel = bool(os.getenv("VERCEL"))
        self.root_dir = "/tmp" if self.on_vercel else os.getcwd()
        base = config.get("downloads_dir", "tmp")
        self.downloads_root = os.path.join(self.root_dir, base)

    def download_episode(
        self, source_url: str, episode_name: str | None
    ) -> Tuple[str, dict]:
        self.source_url = source_url.split("&")[0]
        self.video_id = self.source_url.split("=")[-1]
        mp3 = self._download_file(
            self.config.get("file_ext", DEFAULT_FILE_EXT), audio_only=True
        )
        metadata = self._download_file(
            self.config.get("metadata_ext", DEFAULT_METADATA_EXT)
        )

        try:
            with open(metadata, "r", encoding="utf8") as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to read metadata file: {e}")
            data = {}
        data["video_id"] = self.video_id
        return mp3, data

    def _download_file(self, extension: str, audio_only=False) -> str:
        outdir = os.path.join(self.downloads_root, self.video_id)
        os.makedirs(outdir, exist_ok=True)
        output_template = os.path.join(outdir, f"{self.video_id}{extension}")

        opts = {
            "ffmpeg_location": shutil.which("ffmpeg"),
            "paths": {"home": self.root_dir, "temp": self.root_dir},
            "outtmpl": os.path.join(self.downloads_root, "%(id)s", "%(id)s.%(ext)s"),
            "nocache": True,
        }

        cookiefile = self.config.get("cookies_path")
        if cookiefile:
            opts["cookiefile"] = cookiefile

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

        with YoutubeDL(opts) as ydl:
            ydl.download([self.source_url])

        return output_template
