"""
config.py — Environment configuration for AI Content Engine.
Text generation: OpenRouter (single API key).
Image generation: Pollinations.AI (free, no key).
Video generation: local (imageio, no API).
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "").strip()
if not OPENROUTER_API_KEY:
    raise EnvironmentError("Missing required environment variable: OPENROUTER_API_KEY")

OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-120b:free")
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

IMAGES_DIR: str = "assets/generated_images"
VIDEOS_DIR: str = "assets/generated_videos"
