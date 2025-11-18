"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Existing example schemas (kept for reference)
class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Coliving-specific schemas
class Property(BaseModel):
    """
    Properties collection schema
    Collection name: "property"
    """
    name: str = Field(..., description="Property name")
    location: str = Field(..., description="Neighborhood / Area in Bangalore")
    city: str = Field("Bengaluru", description="City")
    description: str = Field(..., description="Short quirky description")
    amenities: List[str] = Field(default_factory=list, description="List of amenities")
    price_per_month: int = Field(..., ge=0, description="Starting price per bed per month (INR)")
    image_url: Optional[str] = Field(None, description="Hero image URL")
    slug: str = Field(..., description="URL-friendly identifier")

class Inquiry(BaseModel):
    """
    Inquiries collection schema
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Full name of lead")
    email: EmailStr = Field(..., description="Contact email")
    phone: str = Field(..., description="Contact phone number")
    message: Optional[str] = Field(None, description="Message from lead")
    property_slug: Optional[str] = Field(None, description="Slug of the property interested in")
