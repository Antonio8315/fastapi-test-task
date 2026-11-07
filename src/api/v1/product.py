from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.schemas.product import ProductCreate, ProductUpdate, ProductListResponse, ProductDetailResponse
from src.services.product import ProductService

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("", response_model=List[ProductListResponse])
async def get_products(session: AsyncSession = Depends(get_session)):
    from sqlalchemy import select
    from src.models.product import Product
    result = await session.execute(select(Product))
    products = result.scalars().all()
    
    items = []
    for p in products:
        items.append({
            "product_id": p.product_id,
            "name": p.name,
            "category_name": "Категорія",
            "price": p.price
        })
    return items

@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    service = ProductService(session)
    return await service.get_by_id(product_id)

@router.post("", response_model=ProductDetailResponse)
async def create_product(data: ProductCreate, session: AsyncSession = Depends(get_session)):
    service = ProductService(session)
    return await service.create(data)

@router.patch("/{product_id}", response_model=ProductDetailResponse)
async def update_product(product_id: int, data: ProductUpdate, session: AsyncSession = Depends(get_session)):
    service = ProductService(session)
    product = await service.get_by_id(product_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    await session.commit()
    await session.refresh(product)
    return product

@router.delete("/{product_id}")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    service = ProductService(session)
    await service.delete(product_id)
    return {"status": "success"}