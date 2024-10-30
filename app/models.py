from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()

class URLMap(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=True)  # Allowing for custom slug
    clicks = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration time

    @validates('slug')
    def validate_slug(self, key, slug):
        # Ensures the slug is alphanumeric if provided
        if slug and not slug.isalnum():
            raise ValueError("Slug must be alphanumeric")
        return slug
