import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from google import genai
import re

# -------------------------------------------------
# STEP 1: Load Environment Variables
# -------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file!")

# -------------------------------------------------
# STEP 2: Initialize Gemini Client
# -------------------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)


# -------------------------------------------------
# STEP 3: Fetch Trending Topics
# -------------------------------------------------
def fetch_trending_topics():
    """
    Fetch trending topics from Google's Global RSS feed.
    Returns a list of strings.
    """
    url = "https://trends.google.com/trending/rss"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch RSS feed: {response.status_code}")

    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item")
    topics = [item.title.text for item in items[:10]]

    if not topics:
        raise Exception("No topics found in the feed.")

    print(f"✅ Successfully fetched {len(topics)} trending topics (global).")
    return topics


# -------------------------------------------------
# STEP 4: Analyze Topics with Gemini
# -------------------------------------------------
def analyze_topics_with_gemini(topics):
    """
    Use Gemini to analyze trending topics and return structured JSON data.
    """
    print("🤖 Analyzing topics with Gemini...")

    prompt = f"""
    You are an expert SEO strategist and content marketer.
    Analyze these trending topics and rate each (0–100)
    for content potential, monetization value, and long-term SEO performance.

    Return **ONLY valid JSON**, in the format:
    [
      {{
        "topic": "topic_name",
        "score": 0-100,
        "reason": "short explanation"
      }}
    ]

    Topics: {topics}
    """

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = re.sub(r"^```(?:json)?", "", raw_text, flags=re.IGNORECASE).strip()
            raw_text = re.sub(r"```$", "", raw_text).strip()

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            match = re.search(r"\[.*\]", raw_text, re.DOTALL)
            if match:
                parsed = json.loads(match.group())
            else:
                print("⚠️ Gemini returned malformed JSON, saving raw text.")
                parsed = [{"topic": t, "score": 50, "reason": "Default fallback"} for t in topics]

        print(f"✅ Gemini returned {len(parsed)} topics with scores.")
        return parsed

    except Exception as e:
        print(f"❌ Gemini analysis failed: {e}")
        # fallback structure
        return [{"topic": t, "score": 50, "reason": "Default fallback"} for t in topics]


# -------------------------------------------------
# STEP 5: Save Results
# -------------------------------------------------
def save_results(results):
    os.makedirs("data", exist_ok=True)
    file_path = f"data/trends_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved trending analysis → {file_path}")
    return file_path


# -------------------------------------------------
# STEP 6: MAIN EXECUTION
# -------------------------------------------------
if __name__ == "__main__":
    print("🚀 Fetching trending topics...")
    topics = fetch_trending_topics()
    print(f"Found {len(topics)} topics.")
    analyzed = analyze_topics_with_gemini(topics)
    save_results(analyzed)
