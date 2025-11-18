import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import db, create_document, get_documents
from schemas import Property, Inquiry

app = FastAPI(title="Coliving Brand API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def seed_properties_if_empty():
    if db is None:
        return
    count = db["property"].count_documents({})
    if count == 0:
        defaults = [
            {
                "name": "Sunshine Haus",
                "location": "Indiranagar",
                "city": "Bengaluru",
                "description": "Bright, artsy, and a little extra. Rooftop sunsets guaranteed.",
                "amenities": ["High-speed WiFi", "Housekeeping", "Community Events", "Rooftop Lounge"],
                "price_per_month": 17999,
                "image_url": "https://images.unsplash.com/photo-1505691723518-36a5ac3b2d51?q=80&w=1200&auto=format&fit=crop",
                "slug": "sunshine-haus",
            },
            {
                "name": "Yellow Brick",
                "location": "Koramangala 5th Block",
                "city": "Bengaluru",
                "description": "All-day co-work vibes with neon nights. Quirky corners everywhere.",
                "amenities": ["Co-working", "Cafe Machine", "Laundry", "24x7 Power"],
                "price_per_month": 18999,
                "image_url": "https://images.unsplash.com/photo-1554995207-c18c203602cb?q=80&w=1200&auto=format&fit=crop",
                "slug": "yellow-brick",
            },
            {
                "name": "Peppermint Pad",
                "location": "HSR Layout",
                "city": "Bengaluru",
                "description": "Fresh, fun and friendly. Plants, prints and plenty of light.",
                "amenities": ["Gym", "Game Zone", "Chef-on-call", "Bike Parking"],
                "price_per_month": 16999,
                "image_url": "https://images.unsplash.com/photo-1505691723518-36a5ac3b2d51?q=80&w=1200&auto=format&fit=crop",
                "slug": "peppermint-pad",
            },
            {
                "name": "Giggle Grove",
                "location": "Jayanagar",
                "city": "Bengaluru",
                "description": "Community-first living with boardgame battles every weekend.",
                "amenities": ["Events", "Terrace Garden", "Projector", "Library"],
                "price_per_month": 15999,
                "image_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?q=80&w=1200&auto=format&fit=crop",
                "slug": "giggle-grove",
            },
            {
                "name": "Mango Manor",
                "location": "Whitefield",
                "city": "Bengaluru",
                "description": "Sunny balconies, yellow doors and pure chill energy.",
                "amenities": ["Balcony", "AC Rooms", "CCTV", "On-site Support"],
                "price_per_month": 14999,
                "image_url": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?q=80&w=1200&auto=format&fit=crop",
                "slug": "mango-manor",
            },
        ]
        for d in defaults:
            try:
                create_document("property", d)
            except Exception:
                pass


@app.get("/")
def read_root():
    return {"message": "Coliving Brand Backend Running"}


@app.get("/api/properties", response_model=List[Property])
def list_properties() -> List[Property]:
    try:
        seed_properties_if_empty()
        items = get_documents("property", {}, limit=50)
        cleaned: List[Property] = []
        for it in items:
            it.pop("_id", None)
            cleaned.append(Property(**it))
        return cleaned
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/inquiries")
def create_inquiry(payload: Inquiry):
    try:
        create_document("inquiry", payload)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
