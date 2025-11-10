# eBook-Genrerator--BookForge-AI
BookForge AI is a fully autonomous, AI-powered eBook creation system designed to transform real-time web trends into complete, publish-ready eBooks — including content generation, cover design, formatting, and automated cloud upload — all without human input.



📘 BookForge AI
An Autonomous AI System for Generating and Publishing eBooks from Real-Time Web Trends
🧠 Overview

BookForge AI is a fully autonomous, AI-powered eBook creation system designed to transform real-time web trends into complete, publish-ready eBooks — including content generation, cover design, formatting, and automated cloud upload — all without human input.

It operates on a 3-hour cycle, constantly detecting trending topics, analyzing them with Google’s Gemini AI, and producing professionally structured eBooks in both JSON and PDF formats.

Think of it as an AI publishing factory that never sleeps — discovering what people care about right now, and turning that into readable, informative digital books.

🌍 Project Mission

The goal of BookForge AI is to automate the content creation pipeline from trend discovery to book publication — merging the intelligence of AI with automation workflows to build a zero-touch content ecosystem.

It is designed to:

Discover trending topics globally.

Generate structured, SEO-optimized book outlines.

Write full-length, AI-composed eBooks (20–30 pages).

Design beautiful cover images automatically.

Export professional PDFs.

Upload files to Google Drive (or future cloud destinations).

Repeat the cycle every 3 hours autonomously.

🧩 Core Features
Feature	Description
🔍 Trend Detection	Scrapes and analyzes real-time global trends (e.g., Google Trends, Twitter, YouTube) to find top-performing topics.
🧠 SEO Analyzer (Gemini AI)	Uses Google Gemini AI to build rich, SEO-optimized outlines with titles, subtitles, keywords, and chapter structures.
✍️ AI eBook Writer	Expands the outline into a full, multi-chapter eBook with professional tone and logical flow.
🖼️ AI Cover Generator	Automatically fetches or creates cover images using Pixabay API (or fallback to AI-generated visuals).
📘 PDF Generator	Formats and converts eBook JSON into a beautifully structured PDF using custom fonts and styles.
☁️ Google Drive Uploader	Uploads all generated PDFs and JSON files to your Drive folder automatically (with OAuth or Service Account).
🕒 Automation Scheduler	Runs the full process every 3 hours, ensuring BookForge AI continuously produces new eBooks.
🧾 Logging System	Every action and error is logged to logs/bookforge.log for monitoring and debugging.
⚙️ Technical Architecture
┌────────────────────────┐
│  Trend Detector        │  ← Fetches trending topics via APIs & web scraping
└────────────┬───────────┘
             ↓
┌────────────────────────┐
│  SEO Analyzer (Gemini) │  ← Creates structured outlines and chapter ideas
└────────────┬───────────┘
             ↓
┌────────────────────────┐
│  eBook Generator       │  ← Expands outlines into full chapters and summaries
└────────────┬───────────┘
             ↓
┌────────────────────────┐
│  Cover Generator       │  ← Creates AI cover using Pixabay or AI art
└────────────┬───────────┘
             ↓
┌────────────────────────┐
│  PDF Formatter         │  ← Styles, paginates, and exports professional PDF
└────────────┬───────────┘
             ↓
┌────────────────────────┐
│  Google Drive Uploader │  ← Uploads PDFs to user Drive via OAuth/Service Account
└────────────┬───────────┘
             ↓
┌────────────────────────┐
│  Automation Scheduler  │  ← Repeats the process every 3 hours
└────────────────────────┘

🧠 Workflow Summary

Trend Detection

Pulls the latest trending topics from APIs.

Ranks them based on popularity and search frequency.

SEO Outline Generation

Uses Gemini AI to generate:

Book title & subtitle

SEO keywords

10–15 logical chapter titles

Descriptions for each chapter

eBook Creation

Expands each outline into rich, 30-page content.

Formats text, adds summaries, transitions, and structure.

Cover Design

Searches Pixabay (via API) for matching images.

Creates a high-quality cover named after the topic.

PDF Formatting

Converts eBook JSON into a printable, stylized PDF.

Uses DejaVuSans fonts for multilingual text support.

Google Drive Upload

Automatically uploads all generated files to a Drive folder.

Supports both Service Account and OAuth credentials.

Logging & Auto Cycle

Each cycle’s actions are logged into logs/bookforge.log.

The system sleeps for 3 hours and repeats endlessly.

🛠️ Tech Stack
Layer	Technology Used
Language	Python 3.11+
AI Model	Google Gemini 1.5 / Gemini 2 (via google-generativeai)
APIs	Google Drive API, Pixabay API
Automation	Python schedule, time.sleep()
File Handling	JSON, FPDF2 for PDFs, Pillow for images
Data Storage	Local directories (data/ebooks, data/pdfs, etc.)
Environment Management	.env with python-dotenv
Logging	Custom Logger → logs/bookforge.log
Authentication	OAuth 2.0 (Drive), API keys for Pixabay
📁 Project Structure
bookforge-ai/
│
├── agents/
│   ├── trend_detector.py
│   ├── seo_analyzer.py
│   ├── ebook_generator.py
│   ├── cover_generator.py
│   ├── pdf_generator.py
│   ├── drive_uploader.py
│   └── automation_scheduler.py
│
├── assets/
│   ├── DejaVuSans.ttf
│   ├── DejaVuSans-Bold.ttf
│   ├── DejaVuSans-Oblique.ttf
│
├── data/
│   ├── outlines/
│   ├── ebooks/
│   ├── covers/
│   └── pdfs/
│
├── logs/
│   └── bookforge.log
│
├── .env
├── requirements.txt
├── main.py
└── service_account.json

🧾 requirements.txt
python-dotenv==1.0.1
requests==2.31.0
beautifulsoup4==4.12.2
fpdf2==2.7.9
pillow==10.2.0
google-generativeai==0.5.2
tiktoken==0.7.0
pandas==2.2.0
numpy==1.26.3
google-api-python-client==2.120.0
google-auth==2.26.1
google-auth-oauthlib==1.2.0
tqdm==4.66.2
urllib3==2.2.1
colorama==0.4.6
schedule==1.2.1

💡 Innovation Highlights
Innovation	Description
🤖 Full Automation	No manual trigger needed. The system runs autonomously every 3 hours.
🧱 Modular Agents	Each module (trend, SEO, ebook, PDF, upload) is independently replaceable or upgradable.
🧠 AI SEO Optimization	Outlines are generated to maximize search discoverability using AI keyword analysis.
📘 Professional Formatting	The PDF output looks like a real eBook with structured chapters, clean typography, and headers.
☁️ Cloud Integration	Drive upload ensures persistent backups and remote accessibility.
🔄 Zero Downtime	The pipeline continuously monitors, creates, and uploads new eBooks on schedule.
🚀 How to Run the Project
Step 1 — Clone the Repository
git clone https://github.com/yourusername/bookforge-ai.git
cd bookforge-ai

Step 2 — Install Dependencies
pip install -r requirements.txt

Step 3 — Add Environment Variables (.env)
PIXABAY_API_KEY=your_pixabay_key
GOOGLE_API_KEY=your_gemini_key
GOOGLE_DRIVE_FOLDER_ID=your_drive_folder_id

Step 4 — Run the Automation
python main.py

Step 5 — Check Output

eBooks → /data/ebooks

PDFs → /data/pdfs

Covers → /data/covers

Logs → /logs/bookforge.log

🧾 Example Output

Generated PDF:
📕 “Tata Motors Share: A Comprehensive Guide to Investing & Future Growth”
Includes:

10 chapters

Auto-generated summary and analysis

Custom cover image

Formatted layout with headers, spacing, and professional typography

🧠 Future Roadmap
Feature	Description
📰 Auto Blog Publisher	Post book summaries to Medium or WordPress automatically
🎙️ Audio Edition	Convert each eBook into narrated MP3 audiobook
📊 Analytics Dashboard	Web dashboard to visualize generated books and trends
💬 Telegram/Email Alerts	Notify user when new PDFs are uploaded
🌐 Multi-language Mode	Generate books in Hindi, English, Telugu, etc.
🧑‍💻 Marketplace Integration	Publish to Kindle or Gumroad directly
🏆 Conclusion

BookForge AI demonstrates a fully autonomous AI-driven content generation ecosystem, blending trend intelligence, language models, design automation, and cloud integration — all orchestrated through Python.

It’s a step toward next-generation AI publishing — where artificial intelligence acts not just as a tool, but as a self-operating creator, designer, and publisher.
