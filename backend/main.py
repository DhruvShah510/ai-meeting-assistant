from fastapi import FastAPI, HTTPException, UploadFile, File
from groq import Groq
from dotenv import load_dotenv
import os

from schemas import TranscriptRequest, SummaryResponse
from utils import clean_transcript, fix_json_output
from prompts import build_prompt

# Initialize FastAPI
app = FastAPI(
    title="Meeting Summarization API",
    description="AI-powered meeting assistant using Llama 3.3 on Groq",
    version="1.0.0"
)

# Load API Key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.post("/summarize", response_model=SummaryResponse)
async def summarize_meeting(data: TranscriptRequest):
    """
    Accepts meeting transcript as text (JSON)
    """
    try:
        cleaned = clean_transcript(data.transcript_text)
        prompt = build_prompt(cleaned)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        llm_output = response.choices[0].message.content
        parsed_json = fix_json_output(llm_output)

        return SummaryResponse(**parsed_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize-file", response_model=SummaryResponse)
async def summarize_file(file: UploadFile = File(...)):
    """
    Accepts meeting transcript as uploaded .txt file
    """
    try:
        content = await file.read()
        transcript_text = content.decode("utf-8")

        cleaned = clean_transcript(transcript_text)
        prompt = build_prompt(cleaned)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        llm_output = response.choices[0].message.content
        parsed_json = fix_json_output(llm_output)

        return SummaryResponse(**parsed_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
