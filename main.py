from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI()

ads: dict[str, dict] = {}


class AdvertisementCreate(BaseModel):
    title: str
    description: str
    price: float
    author: str


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None


class Advertisement(BaseModel):
    id: str
    title: str
    description: str
    price: float
    author: str
    created_at: str


def to_response(ad_id: str, ad: dict) -> dict:
    return {
        "id": ad_id,
        "title": ad["title"],
        "description": ad["description"],
        "price": ad["price"],
        "author": ad["author"],
        "created_at": ad["created_at"],
    }


@app.post("/advertisement", response_model=Advertisement)
def create_advertisement(body: AdvertisementCreate):
    ad_id = str(uuid.uuid4())
    ads[ad_id] = {
        "title": body.title,
        "description": body.description,
        "price": body.price,
        "author": body.author,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    return to_response(ad_id, ads[ad_id])


@app.get("/advertisement/{advertisement_id}", response_model=Advertisement)
def get_advertisement(advertisement_id: str):
    if advertisement_id not in ads:
        raise HTTPException(status_code=404, detail="Not found")
    return to_response(advertisement_id, ads[advertisement_id])


@app.patch("/advertisement/{advertisement_id}", response_model=Advertisement)
def update_advertisement(advertisement_id: str, body: AdvertisementUpdate):
    if advertisement_id not in ads:
        raise HTTPException(status_code=404, detail="Not found")
    ad = ads[advertisement_id]
    if body.title is not None:
        ad["title"] = body.title
    if body.description is not None:
        ad["description"] = body.description
    if body.price is not None:
        ad["price"] = body.price
    if body.author is not None:
        ad["author"] = body.author
    return to_response(advertisement_id, ad)


@app.delete("/advertisement/{advertisement_id}", status_code=204)
def delete_advertisement(advertisement_id: str):
    if advertisement_id not in ads:
        raise HTTPException(status_code=404, detail="Not found")
    del ads[advertisement_id]
    return None


@app.get("/advertisement")
def search_advertisements(
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    price: Optional[float] = Query(None),
    author: Optional[str] = Query(None),
):
    out = []
    for ad_id, ad in ads.items():
        if title and title not in ad["title"]:
            continue
        if description and description not in ad["description"]:
            continue
        if price is not None and ad["price"] != price:
            continue
        if author and ad["author"] != author:
            continue
        out.append(to_response(ad_id, ad))
    return out
