import os
import json
import shutil
import logging

from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
from imageio_ffmpeg import get_ffmpeg_exe
from models.downloaders.yt_downloader import YT_Downloader
from models.summarizers.openai_summarizer import OpenAI_Summarizer
from models.downloaders.rss_feed_downloader import RSS_Feed_Downloader
from models.transcribers.whisper_transcriber import Whisper_Transcriber


# Load env & config
load_dotenv(override=True)

try:
    with open("config.json") as f:
        config = json.load(f)
except FileNotFoundError:
    raise RuntimeError(
        "config.json file not found. Please provide a valid config.json."
    )
except json.JSONDecodeError:
    raise RuntimeError("config.json is malformed. Please check the file format.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)
logger = logging.getLogger(__name__)


ffmpeg_path = get_ffmpeg_exe()
os.environ["FFMPEG_BINARY"] = ffmpeg_path
os.environ["FFPROBE_BINARY"] = ffmpeg_path

cookie_src = os.path.join(os.getcwd(), config["youtube"]["cookies_path"])
cookie_dst = os.path.join("/tmp", os.path.basename(cookie_src))
shutil.copy(cookie_src, cookie_dst)
config["youtube"]["cookies_path"] = cookie_dst

yt_downloader = YT_Downloader(config=config["youtube"])
transcriber = Whisper_Transcriber(config=config["whisper"])
rss_downloader = RSS_Feed_Downloader(config=config["rss_feed"])
summarizer = OpenAI_Summarizer(config=config["openai"])

app = Flask(__name__)
CORS(app, origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")])


@app.route("/api/summarize", methods=["POST"])
@cross_origin()
def summarize_endpoint():
    """
    Expects JSON with:
      - source_url: str
      - episode_name: str | null
      - detail_level: float (0.0–1.0)
      - platform: "youtube" or "rss"
    Returns JSON with:
      - success: bool
      - summary: str (if success)
      - error: str (if not)
    """
    data = request.get_json()
    source_url = data.get("source_url")
    episode_name = data.get("episode_name")
    detail_level = data.get("detail_level", 0.0)
    platform = data.get("platform")

    # Pick downloader
    if platform == "youtube":
        downloader = yt_downloader
    else:
        downloader = rss_downloader

    try:
        # 1) Download
        mp3_path, metadata = downloader.download_episode(source_url, episode_name)
        logger.info(f"Downloaded {metadata.get('title', '')}")

        # 2) Transcribe
        transcription = transcriber.transcribe(
            audio_path=mp3_path, video_id=metadata["video_id"]
        )

        logger.info("Transcription complete")

        # 3) Summarize
        summary = summarizer.summarize(transcription, detail=detail_level)
        logger.info("Summarization complete")

        return (
            jsonify(
                {
                    "success": True,
                    "title": metadata.get("title", ""),
                    "summary": summary,
                    "thumbnail": metadata.get("thumbnail", ""),
                    "channel": metadata.get("channel", ""),
                    "duration_string": metadata.get("duration_string", ""),
                    "release_date": metadata.get("release_date", ""),
                }
            ),
            200,
        )

    except Exception as e:
        logger.exception("Error in /summarize")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run()
