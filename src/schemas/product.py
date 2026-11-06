from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class ProductAttributeBase(BaseModel):
    group_name: str
    name: str
    value: str
    sort_order: int = 0

class ProductImageBase(BaseModel):
    image: str
    sort_order: int = 0

class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    seo_keyword: Optional[str] = Field(default=None, max_length=255)
    meta_title: Optional[str] = Field(default=None, max_length=255)
    meta_description: Optional[str] = None
    meta_keyword: Optional[str] = Field(default=None, max_length=255)
    image: Optional[str] = Field(default=None, max_length=255)
    status: int = Field(default=0, ge=0, le=1)
    price: float = 0.0
    model: Optional[str] = Field(default=None, max_length=255)
    manufacturer_id: Optional[int] = None

class ProductCreate(ProductBase):
    category_ids: List[int] = []
    attributes: List[ProductAttributeBase] = []
    images: List[ProductImageBase] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    seo_keyword: Optional[str] = Field(default=None, max_length=255)
    meta_title: Optional[str] = Field(default=None, max_length=255)
    meta_description: Optional[str] = None
    meta_keyword: Optional[str] = Field(default=None, max_length=255)
    image: Optional[str] = Field(default=None, max_length=255)
    status: Optional[int] = Field(default=None, ge=0, le=1)
    price: Optional[float] = None
    model: Optional[str] = Field(default=None, max_length=255)
    manufacturer_id: Optional[int] = None

class ProductListResponse(BaseModel):
    product_id: int
    name: str
    category_name: str
    price: float
    
    model_config = ConfigDict(from_attributes=True)

class ProductDetailResponse(ProductBase):
    product_id: int
    rating: float
    viewed: int
    date_added: datetime
    date_modify: datetime
    
    model_config = ConfigDict(from_attributes=True)