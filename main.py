import os
import time
import json
import sys
from datetime import datetime

# Logging setup
os.makedirs("logs", exist_ok=True)
log_file_path = os.path.join("logs", "bookforge.log")

class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass

sys.stdout = Logger(log_file_path)

# --------------------------------------------------
# 🚀 Import Agents
# --------------------------------------------------
from agents.trend_detector import fetch_trending_topics, analyze_topics_with_gemini
from agents.seo_analyzer import generate_outline_for_topic
from agents.ebook_generator import generate_ebook_from_outline
from agents.pdf_generator import generate_pdf_from_ebook
from agents.cover_generator import generate_cover

# Optional Google Drive uploader
try:
    from agents.drive_uploader import upload_to_drive
except ImportError:
    upload_to_drive = None


# --------------------------------------------------
# 🧠 MAIN AUTOMATION FUNCTION
# --------------------------------------------------
def run_full_pipeline():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n📚 Starting BookForge AI full automation pipeline at {timestamp}")
    os.makedirs("data", exist_ok=True)

    # Step 1️⃣ Fetch trending topics
    try:
        topics = fetch_trending_topics()
        print(f"✅ Got {len(topics)} trending topics.")
    except Exception as e:
        print(f"❌ Failed to fetch trending topics: {e}")
        return

    # Step 2️⃣ Analyze topics with Gemini
    try:
        analysis = analyze_topics_with_gemini(topics)
        top_topics = sorted(
            [t for t in analysis if isinstance(t, dict) and "score" in t],
            key=lambda x: x["score"],
            reverse=True
        )[:5]
        print(f"🧠 Selected Top 5 Topics: {[t['topic'] for t in top_topics]}")
    except Exception as e:
        print(f"❌ Topic analysis failed: {e}")
        return

    # Step 3️⃣ Process each topic
    for idx, topic_data in enumerate(top_topics, start=1):
        topic = topic_data.get("topic", "Untitled")
        print(f"\n📘 [{idx}/5] Working on topic: {topic}")

        # SEO Outline
        try:
            outline_data = generate_outline_for_topic(topic)
            if isinstance(outline_data, dict):
                os.makedirs("data/outlines", exist_ok=True)
                safe_name = topic.replace(" ", "_").replace("&", "and").replace("/", "_").lower()
                outline_path = f"data/outlines/{safe_name}_outline.json"
                with open(outline_path, "w", encoding="utf-8") as f:
                    json.dump(outline_data, f, ensure_ascii=False, indent=2)
                print(f"✅ Outline JSON saved → {outline_path}")
            else:
                outline_path = outline_data
        except Exception as e:
            print(f"⚠️ Outline generation failed for '{topic}': {e}")
            continue

        # eBook generation
        try:
            ebook_path = generate_ebook_from_outline(outline_path)
            print(f"✅ eBook JSON saved → {ebook_path}")
        except Exception as e:
            print(f"⚠️ eBook generation failed for '{topic}': {e}")
            continue

        # Cover
        try:
            cover_path = generate_cover(topic)
            print(f"🎨 Cover image ready → {cover_path}")
        except Exception as e:
            print(f"⚠️ Cover generation failed for '{topic}': {e}")

        # PDF
        try:
            pdf_path = generate_pdf_from_ebook(ebook_path)
            print(f"📕 PDF generated → {pdf_path}")
        except Exception as e:
            print(f"⚠️ PDF generation failed for '{topic}': {e}")
            continue

        # Drive Upload
        try:
            folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
            if upload_to_drive and folder_id:
                print("☁️ Uploading to Google Drive...")
                upload_to_drive(pdf_path, folder_id)
            else:
                print("⚠️ Skipping Drive upload (missing credentials or folder ID).")
        except Exception as e:
            print(f"⚠️ Upload failed: {e}")

    print("\n🎉 BookForge AI pipeline complete! All top 5 topics processed.\n")


# --------------------------------------------------
# 🔁 AUTO LOOP EVERY 3 HOURS
# --------------------------------------------------
if __name__ == "__main__":
    print("🚀 BookForge AI Master Automation Initialized.")
    while True:
        run_full_pipeline()
        print("⏳ Sleeping for 3 hours before next cycle...\n")
        time.sleep(3 * 60 * 60)  # 3 hours
