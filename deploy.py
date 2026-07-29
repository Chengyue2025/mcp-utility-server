Here's a production-ready `deploy.py` with FastAPI for serving your MCP server landing page:

```python
#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server Deployment Script
Production-ready FastAPI application with CORS support
"""

import os
import time
import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application configuration
APP_NAME = "MCP Server"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Model Context Protocol Server - AI Model Integration Interface"
START_TIME = time.time()

# Create FastAPI instance
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url=None,  # We'll serve custom docs
    redoc_url=None,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (configure for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)

# HTML Landing Page Template
LANDING_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - {app_version}</title>
    <style>
        :root {{
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --background-color: #f8fafc;
            --card-background: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--background-color);
            color: var(--text-primary);
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 3rem 0;
            margin-bottom: 2rem;
        }}

        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}

        header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .card {{
            background: var(--card-background);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--border-color);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .card h3 {{
            color: var(--primary-color);
            margin-bottom: 0.75rem;
        }}

        .card p {{
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }}

        .card .status {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
        }}

        .status.running {{
            background-color: #dcfce7;
            color: #166534;
        }}

        .status.stopped {{
            background-color: #fef2f2;
            color: #991b1b;
        }}

        .endpoints {{
            background: var(--card-background);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--border-color);
        }}

        .endpoints h2 {{
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}

        .endpoint {{
            display: flex;
            align-items: center;
            padding: 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .endpoint:last-child {{
            border-bottom: none;
        }}

        .method {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            min-width: 60px;
            text-align: center;
            margin-right: 1rem;
        }}

        .method.get {{
            background-color: #dbeafe;
            color: #1e40af;
        }}

        .method.post {{
            background-color: #dcfce7;
            color: #166534;
        }}

        .path {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9rem;
            color: var(--text-primary);
            flex-grow: 1;
        }}

        .description {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-left: 1rem;
        }}

        .footer {{
            text-align: center;
            margin-top: 3rem;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}

        .stats {{
