# 🚀 AI Content Engine

Generate a complete AI-powered marketing campaign — tagline, blog intro, social posts, hero image, and promotional video — from a single brief.

---

## Pipeline Architecture

```
User Input (Product · Audience · Tone)
        │
        ▼
  Campaign Tagline          [OpenRouter · GPT-4.1-mini · Few-shot]
        │
        ▼
  Blog Introduction         [OpenRouter · GPT-4.1-mini · Role Prompting]
        │
        ▼
  Social Media Posts        [OpenRouter · GPT-4.1-mini · Structured JSON Output]
        │
        ▼
  Image Prompt              [Programmatic construction from tone style map]
        │
        ▼
  Hero Image                [FLUX.1-dev · BFL API]
        │
        ▼
  Video Prompt              [Programmatic construction]
        │
        ▼
  Promotional Video (mp4)   [Wan 2.2 I2V · Image-to-Video]
```

---

## Project Structure

```
content_engine/
├── app.py                  # Streamlit UI and pipeline orchestration
├── config.py               # Environment variable loading
├── text_gen.py             # LLM text generation (tagline, blog, social)
├── image_gen.py            # FLUX.1-dev image generation
├── video_gen.py            # Wan 2.2 I2V video generation
├── utils.py                # Retry decorator, JSON parser, file helpers
├── requirements.txt
├── .env.example
├── .gitignore
└── assets/
    ├── generated_images/   # Saved hero images (.jpg)
    └── generated_videos/   # Saved promotional videos (.mp4)
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-org/ai-content-engine.git
cd ai-content-engine/content_engine
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure API Keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
FLUX_API_KEY=your_flux_api_key
WAN_API_KEY=your_wan_api_key
OPENROUTER_MODEL=openai/gpt-4.1-mini
FLUX_MODEL=black-forest-labs/FLUX.1-dev
WAN_MODEL=Wan2.2-I2V
```

| Variable | Where to get it |
|---|---|
| `OPENROUTER_API_KEY` | https://openrouter.ai/keys |
| `FLUX_API_KEY` | https://api.us1.bfl.ai (Black Forest Labs) |
| `WAN_API_KEY` | https://wan-ai.com |

---

## Run the Application

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**.

---

## Usage

1. Enter **Product Name**, **Target Audience**, and select a **Brand Tone** in the sidebar.
2. Click **✨ Generate Campaign**.
3. Watch the pipeline execute sequentially with live progress updates.
4. Download the generated video with the **⬇️ Download Video** button.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit 1.35 |
| LLM | OpenRouter · GPT-4.1-mini |
| Image | FLUX.1-dev (Black Forest Labs) |
| Video | Wan 2.2 I2V (Image-to-Video) |
| Language | Python 3.11+ |

---

## Prompt Engineering Techniques

| Output | Technique |
|---|---|
| Tagline | Few-shot prompting (tone-specific examples) |
| Blog Intro | Role prompting with injected context |
| Social Posts | Structured output (JSON schema enforcement) |
| Image Prompt | Programmatic construction with style map |
| Video Prompt | Cinematic motion descriptor template |
"# Content-Engine" 
