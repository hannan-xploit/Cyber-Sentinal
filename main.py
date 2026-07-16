from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from modules.breach_check import BreachChecker
from modules.ip_reputation import IPReputation
from modules.url_safety import URLSafetyScanner

app = FastAPI(title="CyberIntel Sentinel API", version="2.0")

# Allow frontend to call APIs without blocking (CORS Enabled)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits access from any domain (essential for Vercel)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ONLINE", "message": "CyberIntel Sentinel API Engine Active"}

@app.get("/api/breach")
def check_breach(email: str = Query(..., description="Email target address")):
    return BreachChecker.check_email(email)

@app.get("/api/reputation")
def check_ip(ip: str = Query(..., description="IPv4 target address")):
    return IPReputation.query_ip(ip)

@app.get("/api/safety")
def check_url(url: str = Query(..., description="Target URL/domain")):
    return URLSafetyScanner.analyze_url(url)