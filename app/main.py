from fastapi import FastAPI, HTTPException, Depends, Query, Request
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, conint
from sqlalchemy.orm import Session
import validators
from fastapi.responses import RedirectResponse
from app.database import SessionLocal
from app.models import URLMap
from app.utils import generate_short_code

app = FastAPI()

# Pydantic model for input
# class URLRequest(BaseModel):
#     url: str
#     slug: str = None
#     expires_in_days: conint(ge=0) = None  # Ensure non-negative integer for expiration

@app.post("/url/shorten")
async def shorten_url(request: Request):
    print("Enter api")
    data = await request.json()
    print(data)
    original_url = data.get("url")
    
    custom_slug = data.get("slug")
    expires_in_days = data.get("expires_in_days")

    # Validate the URL format
    if not validators.url(original_url):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    db = SessionLocal()

    # Check for expiration
    expires_at = datetime.now() + timedelta(days=expires_in_days) if expires_in_days is not None else None

    # Check if slug is provided and is unique
    if custom_slug:
        existing_url = db.query(URLMap).filter_by(slug=custom_slug).first()
        if existing_url:
            raise HTTPException(status_code=400, detail="Custom slug is already in use.")

    try:
        # Create and save URL record
        url_record = URLMap(
            original_url=original_url,
            slug=custom_slug,
            expires_at=expires_at,
            clicks=0
        )
        db.add(url_record)
        db.commit()
        db.refresh(url_record)

        # Generate a 10-character short code if slug not provided
        short_code = custom_slug or generate_short_code(10)
        url_record.slug = short_code  # Assign the generated short code to the slug field
        db.commit()

        return {"short_url": f"http://localhost:8000/r/{short_code}"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create short URL")
    finally:
        db.close()

# Redirect and track analytics
@app.get("/r/{slug}")
async def redirect_url(slug: str, db: Session = Depends(SessionLocal)):
    url_data = db.query(URLMap).filter_by(slug=slug).first()

    # Check if URL exists
    if not url_data:
        raise HTTPException(status_code=404, detail="URL not found.")
    
    # Check for expiration
    if url_data.expires_at and datetime.now() > url_data.expires_at:
        raise HTTPException(status_code=410, detail="URL has expired.")

    # Increment click count for analytics
    url_data.clicks += 1
    db.commit()

    return RedirectResponse(url_data.original_url)

# Analytics endpoint
@app.get("/analytics/{slug}")
async def get_analytics(slug: str, db: Session = Depends(SessionLocal)):
    url_data = db.query(URLMap).filter_by(slug=slug).first()
    if not url_data:
        raise HTTPException(status_code=404, detail="URL not found.")
    
    return {
        "original_url": url_data.original_url,
        "clicks": url_data.clicks,
        "expires_at": url_data.expires_at
    }
