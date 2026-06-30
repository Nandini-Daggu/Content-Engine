"""
video_gen.py — Promotional video synthesized locally from the hero image.

Applies a cinematic Ken Burns slow zoom-in effect over 6 seconds at 24fps
using imageio + numpy + Pillow. No external video API required.
"""

import numpy as np
import imageio.v3 as iio
from PIL import Image
from pathlib import Path

import config
from utils import ensure_dirs, timestamped_filename

_FPS = 24
_DURATION_S = 6
_TOTAL_FRAMES = _FPS * _DURATION_S  # 144 frames


def build_video_prompt(product: str, tone: str, tagline: str) -> str:
    """Returns a descriptive label (used in UI only; video is generated locally)."""
    return (
        f"Cinematic slow zoom-in on {product}. "
        f"Tone: {tone}. Tagline: {tagline}. "
        "Ken Burns effect. Smooth cinematic motion. 16:9."
    )


def generate_video(image_path: str, video_prompt: str) -> str:
    """
    Generate a 6-second cinematic MP4 from the hero image using a slow
    Ken Burns zoom-in effect.

    Args:
        image_path:   Local path to the hero image.
        video_prompt: Descriptive label (unused in local generation).

    Returns:
        Local file path to the saved .mp4 video.
    """
    ensure_dirs(config.VIDEOS_DIR)

    # Load and ensure 16:9 at 1280×720
    img = Image.open(image_path).convert("RGB")
    target_w, target_h = 1280, 720
    img = img.resize((target_w, target_h), Image.LANCZOS)
    base = np.array(img, dtype=np.uint8)

    # Ken Burns: start at 100% crop, end at 115% crop (slow zoom-in)
    start_scale = 1.0
    end_scale = 1.15

    filepath = Path(config.VIDEOS_DIR) / timestamped_filename("promo", "mp4")

    with iio.imopen(str(filepath), "w", plugin="pyav") as writer:
        writer.init_video_stream("libx264", fps=_FPS)

        for i in range(_TOTAL_FRAMES):
            t = i / (_TOTAL_FRAMES - 1)  # 0.0 → 1.0
            # ease-in-out: smooth start and end
            t_ease = t * t * (3 - 2 * t)
            scale = start_scale + (end_scale - start_scale) * t_ease

            crop_w = int(target_w / scale)
            crop_h = int(target_h / scale)
            x0 = (target_w - crop_w) // 2
            y0 = (target_h - crop_h) // 2

            cropped = base[y0:y0 + crop_h, x0:x0 + crop_w]
            frame = np.array(
                Image.fromarray(cropped).resize((target_w, target_h), Image.LANCZOS),
                dtype=np.uint8,
            )
            writer.write_frame(frame)

    return str(filepath)
