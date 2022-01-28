from typing import Any, List, Optional
from pydantic import BaseModel


class Site(BaseModel):
    name: str
    url: str


class SiteResponseData(BaseModel):
    url: str


class SiteResponse(BaseModel):
    name: str
    base_url: str
    data: List[SiteResponseData]


class BroadcastItem(BaseModel):
    event: str
    data: List[Any]
    sid: Optional[str]
