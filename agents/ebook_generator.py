import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY missing in .env")

client = genai.Client(api_key=GEMINI_API_KEY)


# --------------------------------------------------
# 🧠 Generate eBook Content
# --------------------------------------------------
def generate_ebook_from_outline(outline_path):
    """
    Reads the SEO or trend JSON and uses Gemini to write full eBook chapters.
    """
    print(f"📖 Loading outline from: {outline_path}")
    if not os.path.exists(outline_path):
        raise FileNotFoundError(f"⚠️ Outline not found at {outline_path}")

    with open(outline_path, "r", encoding="utf-8") as f:
        outline_data = json.load(f)

    # --------------------------------------------------
    # Case 1: It's a trend file (list)
    # --------------------------------------------------
    if isinstance(outline_data, list):
        print("📊 Detected trending topics list — selecting top topic by score...")
        top_topic = max(outline_data, key=lambda x: x.get("score", 0))
        topic = top_topic["topic"]

        print(f"🪄 Generating SEO outline for '{topic}' using Gemini...")
        prompt = f"""
        You are an expert eBook planner and SEO strategist.
        Create a detailed 15-chapter SEO-optimized eBook outline for the topic: {topic}.
        Return JSON in this format:
        {{
          "title": "...",
          "subtitle": "...",
          "topic": "{topic}",
          "chapters": [
            {{
              "chapter_title": "...",
              "description": "..."
            }}
          ]
        }}
        """

        outline_response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        outline_text = outline_response.text.strip()
        try:
            # Try to parse Gemini JSON
            outline_data = json.loads(outline_text.strip("`json\n "))
        except Exception:
            outline_data = {"topic": topic, "chapters": [{"chapter_title": topic, "description": outline_text}]}

    # --------------------------------------------------
    # Case 2: It's already a valid SEO outline
    # --------------------------------------------------
    elif isinstance(outline_data, dict):
        topic = outline_data.get("topic", "Untitled")
    else:
        raise ValueError("❌ Unsupported JSON format for eBook generation.")

    title = outline_data.get("title", topic)
    subtitle = outline_data.get("subtitle", "")
    chapters = outline_data.get("chapters", [])

    print(f"🪄 Generating eBook for topic: {topic}")
    ebook_content = {
        "title": title,
        "subtitle": subtitle,
        "topic": topic,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "chapters": []
    }

    # --------------------------------------------------
    # Generate each chapter
    # --------------------------------------------------
    for idx, ch in enumerate(chapters, start=1):
        chapter_title = ch.get("chapter_title", f"Chapter {idx}")
        description = ch.get("description", "")

        prompt = f"""
        You are a professional eBook writer. Write a detailed, engaging, 
        reader-friendly chapter for the eBook titled "{title}".
        Chapter title: "{chapter_title}"
        Description: {description}
        Write in natural, clear English with real insights and flow.
        """

        print(f"📝 Writing chapter {idx}: {chapter_title}...")
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip() if hasattr(response, "text") else str(response)
        ebook_content["chapters"].append({
            "chapter_title": chapter_title,
            "content": text
        })

    # --------------------------------------------------
    # Save eBook JSON
    # --------------------------------------------------
    os.makedirs("data/ebooks", exist_ok=True)
    output_path = f"data/ebooks/{topic.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ebook_content, f, indent=2, ensure_ascii=False)

    print(f"✅ eBook saved successfully → {output_path}")
    return output_path


# --------------------------------------------------
# ✅ Auto-detect the latest outline and generate eBook
# --------------------------------------------------
if __name__ == "__main__":
    data_dir = "data"
    outline_files = [
        f for f in os.listdir(data_dir)
        if f.endswith(".json") and ("seo" in f.lower() or "trend" in f.lower())
    ]

    if not outline_files:
        raise FileNotFoundError("⚠️ No outline JSON files found in /data folder!")

    # Pick the latest file by modified time
    latest_outline = max(
        [os.path.join(data_dir, f) for f in outline_files],
        key=os.path.getmtime
    )

    print(f"📄 Auto-detected latest outline: {latest_outline}")
    generate_ebook_from_outline(latest_outline)
