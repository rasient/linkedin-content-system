import csv
import shutil
from datetime import date
import streamlit as st
from collections import Counter

from post_manager import load_posts, DB_PATH

st.title("🚀 LinkedIn Content System")

# =========================
# ➕ ADD POST
# =========================

with st.form("add_post"):
    title = st.text_input("Title")
    post_text = st.text_area("Idea")
    topic = st.text_input("Topic")

    if st.form_submit_button("Save"):
        posts = load_posts()
        next_id = str(len(posts) + 1).zfill(3)

        new_post = {
            "post_id": next_id,
            "title": title,
            "post_text": post_text,
            "image_file": "",
            "linkedin_url": "",
            "topic": topic,
            "status": "draft",
            "date": str(date.today()),
            "analytics_file": "",
            "notes": "",
            "generated_post": "",
            "views": 0,
            "likes": 0,
            "comments": 0
        }

        with open(DB_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=new_post.keys())
            writer.writerow(new_post)

        st.success("Saved!")

# =========================
# 📊 DASHBOARD
# =========================

posts = load_posts()

st.header("📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total", len(posts))
col2.metric("Draft", sum(p["status"] == "draft" for p in posts))
col3.metric("Ready", sum(p["status"] == "ready" for p in posts))
col4.metric("Posted", sum(p["status"] == "posted" for p in posts))

# Analytics
st.subheader("📈 Performance")

total_views = sum(int(p.get("views") or 0) for p in posts)
total_likes = sum(int(p.get("likes") or 0) for p in posts)
total_comments = sum(int(p.get("comments") or 0) for p in posts)

st.write(f"Views: {total_views}")
st.write(f"Likes: {total_likes}")
st.write(f"Comments: {total_comments}")

# =========================
# 🧠 STRATEGY
# =========================

st.subheader("🧠 Insights")

posted = [p for p in posts if p["status"] == "posted"]

if posted:
    best = max(posted, key=lambda p: int(p["likes"]) + int(p["comments"]) * 3)
    st.success(f"Best topic: {best['topic']}")