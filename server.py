"""MCP Utility Server — Production Deploy"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="MCP Utility Server")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

INDEX = open("deploy_mcp/index.html",encoding="utf-8").read()

@app.get("/")
async def root():
    return HTMLResponse(INDEX)

@app.get("/health")
async def health():
    return {"status":"healthy","service":"mcp-utility-server","version":"0.1.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
