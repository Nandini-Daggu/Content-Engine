"""
text_gen.py — LLM text generation via OpenRouter with rate-limit-aware
model fallback chain.
"""

import time
import requests
from typing import Any

import config
from utils import parse_json_response

# Models verified working right now — ordered by quality
_FREE_MODELS: list[str] = [
    "openai/gpt-oss-120b:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "google/gemma-4-31b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
]

_TAGLINE_EXAMPLES: dict[str, str] = {
    "Premium":   "Swiss Watch → Time, elevated beyond measure.",
    "Luxury":    "Perfume → Where desire meets eternity.",
    "Eco":       "Bamboo Mug → Sip kindly. Live gently.",
    "Playful":   "Kids Shoes → Run faster, laugh louder.",
    "Modern":    "Smartwatch → The future fits on your wrist.",
    "Minimal":   "Notebook → Less clutter. More clarity.",
    "Corporate": "CRM Tool → Efficiency starts here.",
    "Bold":      "Energy Drink → Unleash what you are.",
    "Elegant":   "Candle → Light that speaks in whispers.",
    "Friendly":  "Coffee → Your best mornings, brewed fresh.",
}


def _chat(system: str, user: str, temperature: float = 0.8) -> str:
    """
    OpenRouter chat with automatic model fallback.
    Skips models that return 429, 402, or null/empty content.
    """
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-content-engine.local",
    }
    payload: dict[str, Any] = {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "max_tokens": 512,
    }

    # Build deduplicated list starting with configured model
    models = list(dict.fromkeys([config.OPENROUTER_MODEL] + _FREE_MODELS))

    for model in models:
        payload["model"] = model
        try:
            resp = requests.post(
                f"{config.OPENROUTER_BASE_URL}/chat/completions",
                headers=headers, json=payload, timeout=60,
            )
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 15))
                time.sleep(min(wait, 20))
                resp = requests.post(
                    f"{config.OPENROUTER_BASE_URL}/chat/completions",
                    headers=headers, json=payload, timeout=60,
                )
            if resp.status_code in (402, 429):
                continue
            resp.raise_for_status()

            content = (
                resp.json()
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content")
            )
            if content:  # skip models that return null/empty content
                return content.strip()
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError):
            pass

    raise RuntimeError(
        "All models are rate-limited. Wait a minute and try again."
    )


def generate_tagline(product: str, audience: str, tone: str) -> str:
    """Generate a campaign tagline using few-shot prompting."""
    example = _TAGLINE_EXAMPLES.get(tone, _TAGLINE_EXAMPLES["Modern"])
    system = (
        f"You are a Creative Director. Reply with ONE tagline, max 10 words, "
        f"no hashtags, no quotes. Tone: {tone}. Example: {example}"
    )
    return _chat(system, f"Product: {product}. Audience: {audience}.", temperature=0.85)


def generate_blog_intro(product: str, audience: str, tone: str, tagline: str) -> str:
    """Generate a 100-word blog introduction using role prompting."""
    system = (
        f"You are a Content Strategist. Write a 100-word blog intro for {product}. "
        f"Tone: {tone}. Audience: {audience}. Include this tagline: {tagline}."
    )
    return _chat(system, "Write the intro.", temperature=0.75)


def generate_social_posts(
    product: str, audience: str, tone: str, tagline: str, blog_intro: str
) -> dict[str, str]:
    """Generate platform social posts as structured JSON output."""
    system = (
        'Return ONLY valid JSON: {"twitter":"","instagram":"","linkedin":""}. '
        "twitter≤280, instagram≤500, linkedin≤300 chars. No markdown."
    )
    user = (
        f"Product: {product}. Tone: {tone}. Tagline: {tagline}. "
        f"Context: {blog_intro[:150]}"
    )
    raw = _chat(system, user, temperature=0.75)
    posts = parse_json_response(raw)
    posts["twitter"]   = posts.get("twitter",   "")[:280]
    posts["instagram"] = posts.get("instagram", "")[:500]
    posts["linkedin"]  = posts.get("linkedin",  "")[:300]
    return posts
