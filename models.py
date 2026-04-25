from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class JobItem(BaseModel):
    title: str
    company: str
    url: HttpUrl
    location: str = "Unknown"
    salary: str = "Not specified"
    published_at: datetime = Field(default_factory=datetime.utcnow)
    meta_hash: str = Field(description="SHA256 хэш для дедупликации")