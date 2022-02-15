from typing import Any, List, Optional
from pydantic import BaseModel
from models import Site as SiteModel, Series,  SiteLink
from tortoise.contrib.pydantic import pydantic_model_creator


class SeriesProcess(BaseModel):
    title: str
    title_eng: str
    poster: str
    site_url: str
    site_link: str


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


SitePydantic = pydantic_model_creator(SiteModel, name='Site')
SeriesPydantic = pydantic_model_creator(Series, name='Series')
SiteLinkPydantic = pydantic_model_creator(SiteLink, name='SiteLink')
