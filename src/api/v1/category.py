from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Literal

from src.db.database import get_session
from src.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryListResponse
from src.services.category import CategoryService

router = APIRouter(prefix="/category", tags=["Category"])

@router.get("", response_model=List[CategoryListResponse])
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: str = None,
    status: int = None,
    sort_by: Literal["name", "id"] = Query("name"),
    sort_order: Literal["asc", "desc"] = Query("asc"),
    session: AsyncSession = Depends(get_session)
):
    service = CategoryService(session)
    return await service.get_list(skip, limit, search, status, sort_by, sort_order)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, session: AsyncSession = Depends(get_session)):
    service = CategoryService(session)
    return await service.get_by_id(category_id)

@router.post("", response_model=CategoryResponse)
async def create_category(data: CategoryCreate, session: AsyncSession = Depends(get_session)):
    service = CategoryService(session)
    return await service.create(data)

@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, data: CategoryUpdate, session: AsyncSession = Depends(get_session)):
    service = CategoryService(session)
    return await service.update(category_id, data)

@router.delete("/{category_id}")
async def delete_category(category_id: int, session: AsyncSession = Depends(get_session)):
    service = CategoryService(session)
    await service.delete(category_id)
    return {"status": "success"}