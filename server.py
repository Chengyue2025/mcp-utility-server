"""MCP Utility Server — Production Server with Payments Integration"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, os

app = FastAPI(title="MCP Utility Server", version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

INDEX = open("index.html",encoding="utf-8").read() if os.path.exists("index.html") else "<h1>MCP Utility Server</h1>"
PRICING = open("pricing.html",encoding="utf-8").read() if os.path.exists("pricing.html") else INDEX

@app.get("/")
async def root():
    return HTMLResponse(INDEX)

@app.get("/pricing")
async def pricing():
    return HTMLResponse(PRICING)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "mcp-utility-server",
        "version": "0.1.0",
        "pricing": {
            "free": {"requests": 100, "price": 0},
            "pro": {"requests": "unlimited", "price": 19.99, "url": "https://buy.stripe.com/test_28o9CJ5aK9hZ3IQ288"},
            "team": {"seats": 5, "price": 49.99, "url": "https://buy.stripe.com/test_28o9CJ5aK9hZ3IQ288"},
        },
        "github": "https://github.com/Chengyue2025/mcp-utility-server",
        "docs": "https://github.com/Chengyue2025/mcp-utility-server#readme",
    }

@app.get("/checkout/{plan}")
async def checkout(plan: str):
    """Redirect to Stripe checkout"""
    urls = {
        "pro": "https://buy.stripe.com/test_28o9CJ5aK9hZ3IQ288",
        "team": "https://buy.stripe.com/test_28o9CJ5aK9hZ3IQ288",
        "donate": "https://buy.stripe.com/test_28o9CJ5aK9hZ3IQ288",
    }
    url = urls.get(plan, urls["pro"])
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url)

@app.get("/api/stats")
async def stats():
    return {
        "uptime": "active",
        "version": "0.1.0",
        "tools": ["web_fetch", "current_time", "calculator"],
        "installation": "pip install mcp-utility-server",
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
