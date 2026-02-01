# api/index.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow any origin
    allow_credentials=False,    # must be False with "*"
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

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/latency", response_model=list[RegionMetricsModel])
def get_region_metrics(data: RegionsThresholdModel):
    df_metrics = pd.read_csv("q-vercel-metrics.csv")
    df_filtered = df_metrics[df_metrics["region"].isin(data.regions)]
    
    result = []
    for region in data.regions:
        df_region = df_filtered[df_filtered["region"] == region]
        if not df_region.empty:
            avg_latency = df_region["latency_ms"].mean()
            p95_latency = df_region["latency_ms"].quantile(0.95)
            avg_uptime = df_region["uptime_percent"].mean()
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
