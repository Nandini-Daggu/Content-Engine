"""
image_gen.py — Hero image generation via Pollinations.AI (free, no API key).

Uses FLUX model. Simple GET request returns JPEG directly.
"""

import re
import time
import requests
from pathlib import Path
from urllib.parse import quote

import config
from utils import retry, ensure_dirs, timestamped_filename

_STYLE_MAP: dict[str, str] = {
    "Premium":   "photorealistic luxury studio",
    "Luxury":    "ultra realistic premium editorial",
    "Eco":       "natural lighting earthy organic",
    "Playful":   "vibrant colorful illustration",
    "Modern":    "minimal futuristic product",
    "Minimal":   "clean white studio",
    "Corporate": "professional commercial",
    "Bold":      "high contrast dramatic lighting",
    "Elegant":   "soft luxury editorial",
    "Friendly":  "warm lifestyle",
}


def build_image_prompt(product: str, tone: str, tagline: str) -> str:
    """Build a concise image generation prompt safe for URL encoding."""
    style = _STYLE_MAP.get(tone, "professional commercial")
    # Keep short and punctuation-light for Pollinations URL stability
    return (
        f"{style} photograph of {product} "
        f"{tagline} centered composition 85mm lens "
        "shallow depth of field studio lighting elegant background "
        "no text no logos high quality commercial"
    )


def _clean_prompt(prompt: str) -> str:
    """Remove characters that cause Pollinations 500 errors."""
    return re.sub(r"[,.:;!?\"'()\[\]{}]", " ", prompt).strip()


@retry(max_attempts=3, base_delay=3.0)
def generate_image(image_prompt: str) -> str:
    """
    Generate a hero image using Pollinations.AI FLUX (free, no API key).

    Returns:
        Local file path to the saved JPEG image.
    """
    ensure_dirs(config.IMAGES_DIR)

    clean = _clean_prompt(image_prompt)
    seed = int(time.time()) % 99999
    url = (
        f"https://image.pollinations.ai/prompt/{quote(clean)}"
        f"?width=1280&height=720&model=flux&nologo=true&seed={seed}"
    )

    resp = requests.get(url, timeout=120)
    resp.raise_for_status()

    filepath = Path(config.IMAGES_DIR) / timestamped_filename("hero", "jpg")
    filepath.write_bytes(resp.content)
    return str(filepath)
