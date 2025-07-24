


# === backend/main.py ===
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os, traceback
from io import BytesIO
from openai import AzureOpenAI
import requests
import fitz  # PyMuPDF

load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_TTS_API_KEY = os.getenv("AZURE_TTS_API_KEY")
AZURE_TTS_API_BASE = os.getenv("AZURE_TTS_API_BASE")
AZURE_TTS_API_VERSION = os.getenv("AZURE_TTS_API_VERSION")
AZURE_TTS_DEPLOYMENT = os.getenv("AZURE_TTS_DEPLOYMENT")

client = AzureOpenAI(api_key=AZURE_API_KEY, api_version=AZURE_API_VERSION, azure_endpoint=AZURE_ENDPOINT)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SpeakRequest(BaseModel):
    text: str
    language: str

class TextSummaryRequest(BaseModel):
    content: str

class PDFUrlRequest(BaseModel):
    pdf_url: str

@app.post("/api/summary-from-text")
def summary_from_text(req: TextSummaryRequest):
    try:
        prompt = "Summarize this webpage content in clear, simple English under 300 words."
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": req.content[:8000]}
        ]
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT_NAME,
            messages=messages,
            temperature=0.5,
            max_tokens=800,
            top_p=0.9
        )
        return {"summary": response.choices[0].message.content.strip()}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Summary error: {str(e)}")

@app.post("/api/speak-line")
def speak(req: SpeakRequest):
    try:
        tts_client = AzureOpenAI(
            api_key=AZURE_TTS_API_KEY,
            api_version=AZURE_TTS_API_VERSION,
            azure_endpoint=AZURE_TTS_API_BASE,
            azure_deployment=AZURE_TTS_DEPLOYMENT
        )
        voice_map = {"en": "nova", "hi": "sunil", "mr": "shreya"}
        voice = voice_map.get(req.language, "nova")
        audio = tts_client.audio.speech.create(
            model=AZURE_TTS_DEPLOYMENT,
            voice=voice,
            input=req.text
        )
        buffer = BytesIO(audio.content)
        return StreamingResponse(buffer, media_type="audio/mpeg")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")

@app.post("/api/summary-from-pdf-url")
def summary_from_pdf_url(req: PDFUrlRequest):
    try:
        response = requests.get(req.pdf_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download PDF")

        with BytesIO(response.content) as pdf_stream:
            doc = fitz.open(stream=pdf_stream.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()

        if not text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in PDF")

        prompt = "Summarize this scientific paper in clear, simple English under 300 words."
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text[:8000]}
        ]
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT_NAME,
            messages=messages,
            temperature=0.5,
            max_tokens=800,
            top_p=0.9
        )

        return {"summary": response.choices[0].message.content.strip()}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF summarization failed: {str(e)}")
