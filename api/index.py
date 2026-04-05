# api/index.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow any origin
    # allow_credentials=False,    # must be False with "*"
    #allow_origins=[
    #   "https://exam.sanand.workers.dev"
    #],
    #allow_credentials=True,
    allow_methods=["*"],        # includes OPTIONS + POST
    allow_headers=["*"],
)

class InferenceRequest(BaseModel):
    audio_id: str
    audio_base64: str

@app.post("/")
def infer(req: InferenceRequest):
    return {
        "rows": 0,
        "columns": [],
        "mean": {},
        "std": {},
        "variance": {},
        "min": {},
        "max": {},
        "median": {},
        "mode": {},
        "range": {},
        "allowed_values": {},
        "value_range": {},
        "correlation": []
    }
  
