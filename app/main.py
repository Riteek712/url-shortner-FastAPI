from fastapi import FastAPI, HTTPException, Depends, Request
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel,Field, conint
from sqlalchemy.orm import Session
import validators
from fastapi.responses import RedirectResponse
from app.database import SessionLocal
from app.models import URLMap
from app.utils import generate_short_code
import re
# Customize FastAPI with Swagger metadata
app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortener service with FastAPI.",
    version="1.0.0"
)

# Define the request body model with examples
class URLRequest(BaseModel):
    url: str = Field(..., example="https://example.com")
    slug: str = Field(None, example="customslug123")
    expires_in_days: conint(ge=0) = Field(None, example=30)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/url/shorten", summary="Shorten a URL", tags=["URL Shortening"])
async def shorten_url(request_body: URLRequest, db: Session = Depends(get_db)):
    """
    Shorten a given URL with an optional custom slug and expiration in days.

    - **url**: The original URL to shorten.
    - **slug**: (Optional) Custom slug to use in the shortened URL.
    - **expires_in_days**: (Optional) Number of days until the URL expires.
    """
    original_url = request_body.url
    custom_slug = request_body.slug
    expires_in_days = request_body.expires_in_days

    # Validate the URL format
    if not validators.url(original_url):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    # Check if slug is alphanumeric if provided
    if custom_slug and not re.match("^[a-zA-Z0-9]*$", custom_slug):
        raise HTTPException(status_code=400, detail="Slug must be alphanumeric only")


    # Check for expiration date
    expires_at = datetime.now() + timedelta(days=expires_in_days) if expires_in_days is not None else None

    # Check if custom slug is unique
    if custom_slug and db.query(URLMap).filter_by(slug=custom_slug).first():
        raise HTTPException(status_code=400, detail="Custom slug is already in use.")

    # Generate a 10-character short code if slug not provided
    short_code = custom_slug or generate_short_code(10)

    try:
        # Create and save URL record
        url_record = URLMap(
            original_url=original_url,
            slug=short_code,
            expires_at=expires_at,
            clicks=0
        )
        db.add(url_record)
        db.commit()
        db.refresh(url_record)

        return {"short_url": f"http://localhost:8000/r/{short_code}"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create short URL")

@app.get("/r/{slug}", summary="Redirect to Original URL", tags=["URL Redirection"])
async def redirect_url(slug: str, db: Session = Depends(get_db)):
    """
    Redirects to the original URL based on the shortened slug.

    - **slug**: The unique identifier of the shortened URL.
    """
    url_data = db.query(URLMap).filter_by(slug=slug).first()

    # Check if URL exists and if it's expired
    if not url_data:
        raise HTTPException(status_code=404, detail="URL not found.")
    if url_data.expires_at and datetime.now() > url_data.expires_at:
        raise HTTPException(status_code=410, detail="URL has expired.")

    # Increment click count
    url_data.clicks += 1
    db.commit()

    return RedirectResponse(url_data.original_url)

@app.get("/analytics/{slug}", summary="Get URL Analytics", tags=["Analytics"])
async def get_analytics(slug: str, db: Session = Depends(get_db)):
    """
    Get analytics data for a shortened URL, including click count and expiration date.

    - **slug**: The unique identifier of the shortened URL.
    """
    url_data = db.query(URLMap).filter_by(slug=slug).first()
    if not url_data:
        raise HTTPException(status_code=404, detail="URL not found.")

    return {
        "original_url": url_data.original_url,
        "clicks": url_data.clicks,
        "expires_at": url_data.expires_at
    }
