# app/main.py
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from app.routes import router_v1

app = FastAPI(title="Core Backend")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Core Backend</title>
        </head>
        <body>
            <h1>Core Backend</h1>
            <p>Backend FastAPI untuk layanan minibank Core yang konek ke middleware.</p>
            <ul>
                <li><strong>Versi:</strong> 1.0.0</li>
                <li><strong>Dokumentasi:</strong> <a href="/docs">/docs</a></li>
            </ul>
            <p><strong>Made with ❤️ by Choco_Mette</strong></p>
            <img src="https://media.tenor.com/8ikVnOwotDQAAAAM/patrick-star-i-love-you.gif" alt="Patrick Star" width="320" height="240" />
        </body>
    </html>
    """
app.include_router(router_v1, prefix="/api/v1")