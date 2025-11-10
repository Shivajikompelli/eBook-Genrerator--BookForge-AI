import os
import json
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv

# Import pipeline modules
from agents.trend_detector import fetch_trending_topics
from agents.seo_analyzer import analyze_seo_and_outline
from agents.cover_generator import generate_cover
from agents.drive_uploader import upload_to_drive

# --------------------------------------------
# STEP 1: Load environment variables
# --------------------------------------------
load_dotenv()

# --------------------------------------------
# STEP 2: Helper function to safely fetch topics
# --------------------------------------------
def safe_fetch_topics():
    topics = fetch_trending_topics()

    # If Gemini returned JSON string → parse it
    if isinstance(topics, str):
        try:
            topics = json.loads(topics)
            print("🔄 Parsed Gemini output string into list successfully.")
        except Exception:
            print("⚠️ Could not parse topics string. Using default fallback.")
            topics = [{"topic": topics, "score": 50, "reason": "fallback"}]

    # Ensure list of dicts
    if not isinstance(topics, list):
        topics = [{"topic": str(topics), "score": 50, "reason": "fallback"}]

    # Convert any plain strings to dicts
    if topics and isinstance(topics[0], str):
        topics = [{"topic": t, "score": 50, "reason": "fallback"} for t in topics]

    return topics


# --------------------------------------------
# STEP 3: eBook generation cycle
# --------------------------------------------
def run_ebook_cycle():
    print(f"\n🚀 Starting automated BookForge cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        topics = safe_fetch_topics()
        if not topics:
            print("⚠️ No trending topics found. Skipping this cycle.")
            return

        # Sort topics by score (highest first)
        topics = sorted(topics, key=lambda x: x.get("score", 0), reverse=True)
        top_topics = topics[:5]

        print(f"🧠 Selected top {len(top_topics)} topics for today's eBooks.")

        # Ensure eBook folder exists
        os.makedirs("data/ebooks", exist_ok=True)

        for i, topic_data in enumerate(top_topics, start=1):
            topic = topic_data.get("topic")
            print(f"\n📘 [{i}/{len(top_topics)}] Generating eBook for: {topic}")

            # Step 1: Generate eBook outline and SEO metadata
            try:
                ebook_json = analyze_seo_and_outline(topic)
            except Exception as e:
                print(f"⚠️ Skipping {topic}: failed to analyze SEO → {e}")
                continue

            if not ebook_json:
                print(f"⚠️ Skipping {topic}: empty content.")
                continue

            # Step 2: Save eBook JSON
            file_name = f"{topic.replace(' ', '_').lower()}_{datetime.now().strftime('%H%M')}.json"
            file_path = os.path.join("data/ebooks", file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(ebook_json, f, indent=2, ensure_ascii=False)
            print(f"✅ eBook JSON saved → {file_path}")

            # Step 3: Generate cover image
            try:
                generate_cover(topic)
            except Exception as e:
                print(f"⚠️ Cover generation failed for {topic}: {e}")

            # Step 4: Upload to Google Drive
            try:
                folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
                upload_to_drive(file_path, folder_id)
            except Exception as e:
                print(f"⚠️ Upload failed for {topic}: {e}")

        print("\n✅ Completed this eBook generation cycle.")

    except Exception as e:
        print(f"❌ Automation cycle failed: {e}")


# --------------------------------------------
# STEP 4: Scheduler Setup
# --------------------------------------------
if __name__ == "__main__":
    print("📅 BookForge AI Automation Scheduler initialized.")
    print("⏰ Will generate 5 new eBooks every 3 hours automatically.\n")

    # Schedule every 3 hours
    schedule.every(3).hours.do(run_ebook_cycle)

    # Run immediately for first time
    run_ebook_cycle()

    # Keep running forever
    while True:
        schedule.run_pending()
        time.sleep(60)
