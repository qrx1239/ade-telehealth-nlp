# ade-telehealth-nlp# ADE Telehealth NLP

A clinical NLP prototype built to analyze pharmacist-patient telehealth conversations and identify possible adverse drug events from unstructured patient language.

## What it does

- Detects adverse events from transcript text
- Handles negation such as “no vomiting”
- Identifies timing context such as “since starting treatment”
- Flags medication mentions
- Stratifies overall severity as mild, moderate, or severe
- Detects serious adverse event criteria such as ER visits, hospitalization, or life-threatening symptoms
- Supports batch analysis of multiple transcripts

## Example use case

Input:
“I’ve had really bad diarrhea and some tingling in my feet since starting treatment. No vomiting.”

Output:
- diarrhea = present
- neuropathy = present
- vomiting = negated
- severity = moderate
- serious adverse event = false

## Files

- `app.py` — FastAPI endpoints for single and batch transcript analysis
- `nlp_logic.py` — core NLP and rule-based classification logic
- `sample_transcripts.json` — example pharmacist-patient conversations

## Endpoints

### `POST /analyze`
Analyze one transcript.

### `POST /batch_analyze`
Analyze multiple transcripts and return summary counts.

## Why I built this

This project was inspired by real specialty pharmacy follow-up workflows where adverse events must be recognized quickly, documented accurately, and sometimes escalated to pharmaceutical manufacturers within strict timelines.

## Future improvements

- Per-symptom severity scoring
- Drug-specific adverse event mapping
- Dashboard for batch transcript review
- More advanced NLP models beyond rule-based matching
