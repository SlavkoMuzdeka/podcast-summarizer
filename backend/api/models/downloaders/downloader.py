from typing import Tuple
from abc import ABC, abstractmethod


class Downloader(ABC):
    @abstractmethod
    def download_episode(
        self, source_url: str, episode_name: str | None
    ) -> Tuple[str, dict]:
        pass
