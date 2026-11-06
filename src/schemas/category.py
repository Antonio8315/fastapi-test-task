from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    seo_keyword: Optional[str] = Field(default=None, max_length=255)
    meta_title: Optional[str] = Field(default=None, max_length=255)
    meta_description: Optional[str] = None
    meta_keyword: Optional[str] = Field(default=None, max_length=255)
    image: Optional[str] = Field(default=None, max_length=255)
    status: int = Field(default=1, ge=0, le=1)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    parent_category_id: Optional[int] = None
    seo_keyword: Optional[str] = Field(default=None, max_length=255)
    meta_title: Optional[str] = Field(default=None, max_length=255)
    meta_description: Optional[str] = None
    meta_keyword: Optional[str] = Field(default=None, max_length=255)
    image: Optional[str] = Field(default=None, max_length=255)
    status: Optional[int] = Field(default=None, ge=0, le=1)

class CategoryResponse(CategoryBase):
    category_id: int
    date_added: datetime
    date_modify: datetime
    model_config = ConfigDict(from_attributes=True)

class CategoryListResponse(BaseModel):
    category_id: int
    name: str
    status: int
    
    model_config = ConfigDict(from_attributes=True)
