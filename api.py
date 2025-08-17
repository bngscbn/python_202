# api.py
from __future__ import annotations
from fastapi import FastAPI

app = FastAPI(title="Py202 Library API", version="1.0.0")

# Basit sağlık kontrolü: sunucu ayakta mı?
@app.get("/health")
def health():
    return {"status": "ok"}