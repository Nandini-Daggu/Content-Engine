"""
app.py — AI Content Engine · Streamlit Application Entry Point.
"""

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="AI Content Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

from text_gen import generate_tagline, generate_blog_intro, generate_social_posts
from image_gen import build_image_prompt, generate_image
from video_gen import build_video_prompt, generate_video

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎯 Campaign Brief")
    st.markdown("---")
    product  = st.text_input("Product Name",    placeholder="e.g. AuraGlow Serum")
    audience = st.text_input("Target Audience", placeholder="e.g. Women 25–40, skincare enthusiasts")
    tone = st.selectbox(
        "Brand Tone",
        ["Premium","Luxury","Eco","Playful","Modern","Minimal","Corporate","Bold","Elegant","Friendly"],
    )
    st.markdown("---")
    generate_btn = st.button("✨ Generate Campaign", use_container_width=True, type="primary")

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🚀 AI Content Engine")
st.caption("Generate a complete marketing campaign from a single brief.")

# ── Pipeline ─────────────────────────────────────────────────────────────────
if generate_btn:
    if not product.strip() or not audience.strip():
        st.error("Please fill in both **Product Name** and **Target Audience**.")
        st.stop()

    col_left, col_right = st.columns(2, gap="large")
    progress = st.progress(0, text="Starting…")

    def step(n: int, label: str) -> None:
        progress.progress(int(n / 7 * 100), text=label)

    try:
        # Step 1 — Tagline
        step(0, "Generating tagline…")
        with col_left:
            with st.spinner("Crafting tagline…"):
                tagline = generate_tagline(product, audience, tone)
            st.success("✅ Campaign Tagline")
            st.markdown(f"### ✨ _{tagline}_")

        # Step 2 — Blog intro
        step(1, "Generating blog introduction…")
        with col_left:
            with st.spinner("Writing blog introduction…"):
                blog_intro = generate_blog_intro(product, audience, tone, tagline)
            st.success("✅ Blog Introduction")
            with st.expander("📝 Blog Introduction", expanded=True):
                st.write(blog_intro)

        # Step 3 — Social posts
        step(2, "Generating social media posts…")
        with col_left:
            with st.spinner("Creating social posts…"):
                posts = generate_social_posts(product, audience, tone, tagline, blog_intro)
            st.success("✅ Social Media Posts")
            with st.expander("📱 Social Media Posts", expanded=True):
                st.markdown("**𝕏 Twitter / X**");  st.info(posts.get("twitter", ""))
                st.markdown("**📸 Instagram**");    st.info(posts.get("instagram", ""))
                st.markdown("**💼 LinkedIn**");     st.info(posts.get("linkedin", ""))

        # Step 4 — Hero image
        step(3, "Building image prompt…")
        image_prompt = build_image_prompt(product, tone, tagline)
        step(4, "Generating hero image (30–60 s)…")
        with col_right:
            with st.spinner("Generating hero image with FLUX.1-dev…"):
                image_path = generate_image(image_prompt)
            st.success("✅ Hero Image")
            st.image(image_path, caption=f"Hero Image · {product}", use_container_width=True)

        # Step 5 — Promotional video
        step(5, "Building video prompt…")
        video_prompt = build_video_prompt(product, tone, tagline)
        step(6, "Generating promotional video (2–3 min)…")
        with col_right:
            with st.spinner("Generating video with Wan 2.2 I2V…"):
                video_path = generate_video(image_path, video_prompt)
            st.success("✅ Promotional Video")
            st.video(video_path)
            with open(video_path, "rb") as vf:
                st.download_button(
                    "⬇️ Download Video", vf,
                    file_name=Path(video_path).name,
                    mime="video/mp4",
                    use_container_width=True,
                )

        progress.progress(100, text="🎉 Campaign complete!")
        st.balloons()

    except RuntimeError as exc:
        progress.empty()
        st.error(f"**Generation failed:** {exc}")
    except Exception as exc:
        progress.empty()
        st.error(f"**Unexpected error:** {exc}")

else:
    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        st.info("👈 Fill in the campaign brief and click **Generate Campaign**.")
    with col_right:
        st.info("🖼️ Your hero image and promotional video will appear here.")
