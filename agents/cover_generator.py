import os
import requests
import time
from dotenv import load_dotenv
from datetime import datetime
import shutil

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# 🎨 Generate Cover Function
# --------------------------------------------------
def generate_cover(topic):
    """
    Generates a book cover image for the given topic.
    Priority:
    1️⃣ Pixabay API (if available)
    2️⃣ Unsplash fallback
    3️⃣ Local default cover (assets/default_cover.jpg)
    """
    print(f"🎨 Generating cover image for: {topic}")

    # Prepare directories
    os.makedirs("data/covers", exist_ok=True)
    output_path = f"data/covers/{topic.replace(' ', '_').lower()}_cover.jpg"

    # --------------------------------------------------
    # 1️⃣ Attempt Pixabay (most reliable)
    # --------------------------------------------------
    try:
        PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")
        if PIXABAY_API_KEY:
            search_query = topic.replace(" ", "+")
            pixabay_url = (
                f"https://pixabay.com/api/?key={PIXABAY_API_KEY}"
                f"&q={search_query}&image_type=photo&orientation=square"
            )
            print(f"🔍 Searching Pixabay: {pixabay_url}")
            response = requests.get(pixabay_url, timeout=10).json()

            if response.get("hits"):
                img_url = response["hits"][0]["largeImageURL"]
                img_data = requests.get(img_url, timeout=15)
                if img_data.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(img_data.content)
                    print(f"✅ Pixabay cover saved → {output_path}")
                    return output_path
            else:
                print("⚠️ Pixabay returned no matching results. Retrying with a broader query...")

                # 🔄 Broader fallback: search with generic keywords
                fallback_url = (
                    f"https://pixabay.com/api/?key={PIXABAY_API_KEY}"
                    f"&q=horoscope+astrology+zodiac+stars&image_type=photo&orientation=square"
                )

                fallback_response = requests.get(fallback_url, timeout=10).json()
                if fallback_response.get("hits"):
                    img_url = fallback_response["hits"][0]["largeImageURL"]
                    img_data = requests.get(img_url, timeout=15)
                    if img_data.status_code == 200:
                        with open(output_path, "wb") as f:
                            f.write(img_data.content)
                        print(f"✅ Fallback Pixabay cover saved → {output_path}")
                        return output_path
                else:
                    print("⚠️ Fallback Pixabay also returned no results.")
        else:
            print("⚠️ No Pixabay API key found in .env (skipping to Unsplash).")
    except Exception as e:
        print(f"❌ Pixabay failed: {e}")

    # --------------------------------------------------
    # 2️⃣ Fallback: Unsplash
    # --------------------------------------------------
    try:
        unsplash_url = f"https://source.unsplash.com/1024x1024/?{topic},book,art,illustration"
        print(f"🔍 Pulling from Unsplash: {unsplash_url}")

        for attempt in range(3):
            img_response = requests.get(unsplash_url, timeout=15)
            if img_response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                print(f"✅ Unsplash cover saved on attempt {attempt+1} → {output_path}")
                return output_path
            else:
                print(f"⚠️ Attempt {attempt+1} failed ({img_response.status_code}), retrying...")
                time.sleep(5)
    except Exception as e:
        print(f"❌ Unsplash fallback failed: {e}")

    # --------------------------------------------------
    # 3️⃣ Final fallback: Local placeholder
    # --------------------------------------------------
    try:
        local_fallback = "assets/default_cover.jpg"
        if os.path.exists(local_fallback):
            shutil.copy(local_fallback, output_path)
            print(f"✅ Default local cover used → {output_path}")
            return output_path
        else:
            print("⚠️ Local fallback cover not found in assets/.")
    except Exception as e:
        print(f"❌ Failed to copy local fallback: {e}")

    print("⚠️ No cover generated, continuing without image.")
    return None


# --------------------------------------------------
# ✅ Test Directly
# --------------------------------------------------
if __name__ == "__main__":
    test_topic = "Saptahik Rashifal: Your Weekly Horoscope Guide"
    generate_cover(test_topic)
