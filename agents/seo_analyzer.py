# import os
# import json
# from datetime import datetime
# from dotenv import load_dotenv
# from google import genai

# # ---------------------------------------
# # Step 1: Load environment and init Gemini
# # ---------------------------------------
# load_dotenv()
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# # ---------------------------------------
# # Step 2: Get Latest Trends File
# # ---------------------------------------
# def get_latest_trend_file():
#     data_folder = "data"
#     files = [f for f in os.listdir(data_folder) if f.startswith("trends_")]
#     if not files:
#         raise FileNotFoundError("No trend files found in /data/. Run trend_detector.py first.")
#     latest = max(files)
#     return os.path.join(data_folder, latest)

# # ---------------------------------------
# # Step 3: Load Trending Topics
# # ---------------------------------------
# def load_trending_data():
#     with open(get_latest_trend_file(), "r", encoding="utf-8") as f:
#         data = json.load(f)
#     if "raw_response" in data:
#         raise ValueError("⚠️ The last trend data was not parsed as valid JSON.")
#     return data

# # ---------------------------------------
# # Step 4: Generate Outline from Top Topic
# # ---------------------------------------
# import re
# import json

# def generate_outline(topic):
#     print(f"🧠 Generating eBook structure for topic: {topic['topic']}")

#     prompt = f"""
#     You are an expert eBook creator and SEO strategist.

#     Based on the topic "{topic['topic']}", create:
#     1. An SEO-optimized eBook title
#     2. A subtitle with emotional and search appeal
#     3. 8–15 relevant keywords
#     4. A detailed outline with 10–15 chapters, each with a short description

#     Return only valid JSON in this format:
#     {{
#       "title": "string",
#       "subtitle": "string",
#       "keywords": ["string", ...],
#       "chapters": [
#         {{
#           "chapter_title": "string",
#           "description": "string"
#         }}
#       ]
#     }}
#     """

#     response = client.models.generate_content(
#         model="models/gemini-2.5-flash",
#         contents=prompt
#     )

#     raw = response.text.strip()

#     # 🔧 Step 1: Clean markdown wrappers
#     if raw.startswith("```"):
#         raw = re.sub(r"^```(?:json)?", "", raw, flags=re.IGNORECASE).strip()
#         raw = re.sub(r"```$", "", raw).strip()

#     # 🔧 Step 2: Try to extract JSON
#     try:
#         outline = json.loads(raw)
#     except json.JSONDecodeError:
#         # Try to locate JSON inside text
#         match = re.search(r"\{.*\}|\[.*\]", raw, re.DOTALL)
#         if match:
#             try:
#                 outline = json.loads(match.group())
#             except Exception:
#                 outline = {"topic": topic["topic"], "raw_response": raw}
#         else:
#             outline = {"topic": topic["topic"], "raw_response": raw}

#     # 🔧 Step 3: Attach topic name
#     if "topic" not in outline:
#         outline["topic"] = topic["topic"]

#     return outline

# # ---------------------------------------
# # Step 5: Save Outline
# # ---------------------------------------
# def save_outline(outline):
#     os.makedirs("data/outlines", exist_ok=True)
#     topic_name = outline.get("topic", "unknown").replace(" ", "_")[:30]
#     file_path = f"data/outlines/outline_{topic_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
#     with open(file_path, "w", encoding="utf-8") as f:
#         json.dump(outline, f, indent=2, ensure_ascii=False)
#     print(f"✅ Outline saved to {file_path}")

# # ---------------------------------------
# # Step 6: Main
# # ---------------------------------------
# if __name__ == "__main__":
#     print("🚀 Starting SEO Analyzer + Outline Generator...")
#     topics = load_trending_data()
#     top_topic = max(topics, key=lambda x: x.get("score", 0))
#     print(f"📈 Top topic selected: {top_topic['topic']} (Score: {top_topic['score']})")
#     outline = generate_outline(top_topic)
#     save_outline(outline)
# import os
# import json
# from datetime import datetime
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# # Initialize Gemini client
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# os.makedirs("data", exist_ok=True)

# # -------------------------------------------------------
# # ✅ FUNCTION: analyze_seo_and_outline()
# # -------------------------------------------------------
# def analyze_seo_and_outline(topic):
#     """
#     Given a topic, analyze SEO potential and generate
#     eBook title, subtitle, keywords, and chapter outline.
#     Returns a dictionary with all fields.
#     """
#     print(f"🤖 Analyzing SEO and outline for topic: {topic}")

#     prompt = f"""
#     You are an expert SEO strategist and eBook planner.
#     Analyze the topic '{topic}' and generate:
#     1. A powerful eBook title (SEO optimized)
#     2. A catchy subtitle
#     3. 10–15 relevant SEO keywords
#     4. 10–15 descriptive chapter titles with short summaries
#     Return valid JSON only in this format:
#     {{
#       "title": "string",
#       "subtitle": "string",
#       "keywords": ["list", "of", "keywords"],
#       "chapters": [
#         {{"chapter_title": "string", "description": "string"}}
#       ]
#     }}
#     """

#     try:
#         response = client.models.generate_content(
#             model="models/gemini-2.5-flash",
#             contents=prompt
#         )

#         raw_text = response.text.strip()

#         # Some responses may include ```json ... ```
#         if raw_text.startswith("```"):
#             raw_text = raw_text.split("```json")[-1].split("```")[-2].strip()

#         data = json.loads(raw_text)

#         filename = f"data/seo_{topic.replace(' ', '_')}_{datetime.now().strftime('%H%M')}.json"
#         with open(filename, "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=2, ensure_ascii=False)

#         print(f"✅ SEO analysis saved: {filename}")
#         return data

#     except Exception as e:
#         print(f"⚠️ Gemini SEO analysis failed: {e}")
#         return {
#             "title": topic.title(),
#             "subtitle": f"Insights and guide on {topic}",
#             "keywords": [topic],
#             "chapters": [{"chapter_title": "Introduction", "description": "Overview of the topic"}],
#         }


# # -------------------------------------------------------
# # 🧠 Optional Test Run
# # -------------------------------------------------------
# if __name__ == "__main__":
#     topic = "saptahik rashifal"
#     result = analyze_seo_and_outline(topic)
#     print(json.dumps(result, indent=2, ensure_ascii=False))
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# ⚙️ Setup
# --------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env!")

client = genai.Client(api_key=GEMINI_API_KEY)


# --------------------------------------------------
# 🧩 Generate SEO + Outline
# --------------------------------------------------
def generate_outline_for_topic(topic: str):
    """
    Uses Gemini to generate a structured SEO outline
    for the given topic. Returns a dict.
    """

    print(f"🤖 Analyzing SEO and outline for topic: {topic}")

    prompt = f"""
    You are an SEO strategist and professional eBook planner.
    Create a detailed SEO-optimized eBook outline for the topic:
    "{topic}"

    Your response must be in **strict JSON** format:
    {{
      "topic": "{topic}",
      "title": "Readable, catchy eBook title",
      "subtitle": "Short, attractive subtitle",
      "keywords": ["keyword1", "keyword2", ...],
      "chapters": [
        {{
          "chapter_title": "Title 1",
          "description": "Short 1–2 sentence summary"
        }},
        {{
          "chapter_title": "Title 2",
          "description": "Short summary"
        }}
      ]
    }}
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    raw_text = response.text.strip() if hasattr(response, "text") else str(response)

    # Clean markdown artifacts (```json ... ```)
    import re
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?", "", raw_text).strip()
        raw_text = re.sub(r"```$", "", raw_text).strip()

    # Parse JSON safely
    try:
        parsed = json.loads(raw_text)
    except Exception:
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
            except:
                parsed = {"topic": topic, "raw_response": raw_text}
        else:
            parsed = {"topic": topic, "raw_response": raw_text}

    return parsed


# --------------------------------------------------
# 🧪 Test Run (for debugging)
# --------------------------------------------------
if __name__ == "__main__":
    test_topic = "Saptahik Rashifal: Your Weekly Horoscope Guide"
    outline = generate_outline_for_topic(test_topic)
    os.makedirs("data", exist_ok=True)
    file_path = f"data/seo_{test_topic.replace(' ', '_').lower()}_{datetime.now().strftime('%H%M')}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(outline, f, indent=2, ensure_ascii=False)
    print(f"✅ Outline saved → {file_path}")
