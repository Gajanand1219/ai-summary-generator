# 🧠 AI Summary Generator

AI-powered tool to summarize content from any webpage or uploaded PDF using GPT (via OpenAI or Azure OpenAI).  
Supports both API usage and a Chrome extension for one-click summarization.

---

## 🚀 Features

- 🌍 Summarize any webpage by providing a URL
- 📄 Upload PDF files and get summarized text
- 🧩 Chrome Extension to summarize the current tab with one click
- ⚙️ Built with Python (Flask), OpenAI, BeautifulSoup, PyPDF2

---


## 🚀 How to Use the Extension
https://youtu.be/gtF2nHVjqFk?si=qMS_hs7wJJ1ShJMb

### Step 1: Load Locally in Chrome

1. Open Chrome
2. Go to: `chrome://extensions/`
3. Enable **Developer Mode** (top right)
4. Click **Load unpacked**
5. Select the `youtube-summary-extension/` folder

---

## 🧪 How It Works

- `content.js` injects a "Summarize" button into YouTube pages
- On click, it:
  - Extracts video ID or transcript
  - Sends data to your backend API (e.g., Flask or FastAPI)
  - Receives the AI-generated summary
  - Displays it in a simple popup (`popup.html`)

---
![WhatsApp Image 2025-06-25 at 18 27 49_bc85b557](https://github.com/user-attachments/assets/4a9bc2ff-05c0-4b9a-b90e-6e5fe73143e1)

![WhatsApp Image 2025-06-25 at 18 27 49_1400f5c1](https://github.com/user-attachments/assets/8851300c-5df8-47f5-889c-df188bc127e7)


## ⚙️ Backend Setup

### 🐍 1. Create a virtual environment

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or `venv\Scripts\activate` on Windows


## 🗂️ Project Structure
ai-summary-generator/
├── backend/ # Python Flask API
│ ├── main.py # Core backend logic
│ ├── .env # API keys and environment configs
│ ├── requirements.txt # Python dependencies
│ └── venv/ # Virtual environment (excluded from git)
│
├── chrome-extension/ # Chrome Extension (optional)
│ ├── manifest.json
│ ├── popup.html
│ ├── popup.js
│ ├── icon.png
│ └── styles.css
│
└── README.md # You're reading it

---

