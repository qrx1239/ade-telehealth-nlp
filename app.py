from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from nlp_logic import analyze_text

app = FastAPI(title="ADE Telehealth NLP API")


class TranscriptRequest(BaseModel):
    text: str


class BatchTranscriptRequest(BaseModel):
    id: Optional[int] = None
    text: str


@app.get("/")
def home():
    return {"message": "ADE Telehealth NLP API is running"}


@app.post("/analyze")
def analyze(request: TranscriptRequest):
    return analyze_text(request.text)


@app.post("/batch_analyze")
def batch_analyze(requests: List[BatchTranscriptRequest]):
    results = []
    mild = 0
    moderate = 0
    severe = 0
    serious = 0

    for item in requests:
        analysis = analyze_text(item.text)

        if analysis["severity"] == "mild":
            mild += 1
        elif analysis["severity"] == "moderate":
            moderate += 1
        elif analysis["severity"] == "severe":
            severe += 1

        if analysis["serious_adverse_event"]:
            serious += 1

        results.append({
            "id": item.id,
            "analysis": analysis
        })

    return {
        "count": len(results),
        "summary": {
            "mild": mild,
            "moderate": moderate,
            "severe": severe,
            "serious_adverse_events": serious
        },
        "results": results
    }
