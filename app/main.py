from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.models import URLMap
from app.database import SessionLocal
from app.utils import encode_url
from sqlalchemy.exc import IntegrityError
import validators

app = FastAPI()

@app.post("/url/shorten")
async def shorten_url(request: Request):
    data = await request.json()
    print(data)
    original_url = data.get("url")
    
    if not original_url or not validators.url(original_url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    db = SessionLocal()
    try:
        url_record = URLMap(original_url=original_url)
        db.add(url_record)
        db.commit()
        db.refresh(url_record)
        short_code = encode_url(url_record.id)
        url_record.short_url = short_code
        db.commit()
        return {"short_url": f"http://localhost:8000/r/{short_code}"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create short URL")
    finally:
        db.close()

@app.get("/r/{short_code}")
async def redirect_url(short_code: str):
    db = SessionLocal()
    try:
        url_record = db.query(URLMap).filter(URLMap.short_url == short_code).first()
        if not url_record:
            raise HTTPException(status_code=404, detail="Short URL not found")
        return RedirectResponse(url_record.original_url, status_code=302)
    finally:
        db.close()
