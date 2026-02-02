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
    # allow_origins=[
    #    "https://exam.sanand.workers.dev"
    #],
    #allow_credentials=True,
    allow_methods=["*"],        # includes OPTIONS + POST
    allow_headers=["*"],
)

# Request body schema
class RegionsThresholdModel(BaseModel):
    regions: list[str]
    threshold_ms: int = 180

class RegionMetricsModel(BaseModel):
    region: str
    avg_latency: float
    p95_latency: float
    avg_uptime: float
    breaches: int

@app.api_route("/", methods=["GET", "POST", "OPTIONS", "HEAD"])
async def root():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Handle POST + OPTIONS preflight
@app.api_route("/api/latency", methods=["GET", "POST", "OPTIONS"])
async def latency(request: Request):
    if request.method == "OPTIONS":
        # Preflight request
        return JSONResponse({}, status_code=204)

    # Parse JSON body for POST
    payload = await request.json() if request.method == "POST" else {}

    # Example response (replace with real logic)
    response_data = [
        {"region":"emea","avg_latency":175.31,"p95_latency":225.49,"avg_uptime":98.33,"breaches":6},
        {"region":"apac","avg_latency":157.55,"p95_latency":200.61,"avg_uptime":98.11,"breaches":2}
    ]

    return JSONResponse(response_data)

@app.post("/api/latency", response_model=list[RegionMetricsModel])
def get_region_metrics(data: RegionsThresholdModel):
    df_metrics = pd.read_json("q-vercel-latency.json")
    df_filtered = df_metrics[df_metrics["region"].isin(data.regions)]
    
    result = []
    for region in data.regions:
        df_region = df_filtered[df_filtered["region"] == region]
        if not df_region.empty:
            avg_latency = df_region["latency_ms"].mean()
            p95_latency = df_region["latency_ms"].quantile(0.95)
            avg_uptime = df_region["uptime_pct"].mean()
            breaches = (df_region["latency_ms"] > data.threshold_ms).sum()
            
            region_metrics = RegionMetricsModel(
                region=region,
                avg_latency=avg_latency,
                p95_latency=p95_latency,
                avg_uptime=avg_uptime,
                breaches=breaches
            )
            result.append(region_metrics)
    
    return result


