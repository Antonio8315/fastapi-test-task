from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from src.models.category import Category
from src.schemas.category import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_full_paths_map(self) -> dict[int, str]:
        result = await self.session.execute(select(Category))
        categories = result.scalars().all()
        
        cat_dict = {c.category_id: c for c in categories}
        paths_map = {}

        for cat in categories:
            path_parts = [cat.name]
            parent_id = cat.parent_category_id
            
            while parent_id and parent_id in cat_dict:
                parent = cat_dict[parent_id]
                path_parts.append(parent.name)
                parent_id = parent.parent_category_id
                
            paths_map[cat.category_id] = " > ".join(reversed(path_parts))
            
        return paths_map

    async def get_list(self, skip: int = 0, limit: int = 10, search: str = None, status: int = None, sort_by: str = "name", sort_order: str = "asc"):
        result = await self.session.execute(select(Category))
        categories = result.scalars().all()
        paths_map = await self.get_full_paths_map()

        items = []
        for cat in categories:
            items.append({
                "category_id": cat.category_id,
                "name": paths_map[cat.category_id],
                "status": cat.status
            })

        if status is not None:
            items = [item for item in items if item["status"] == status]

        if search:
            search_lower = search.lower()
            items = [
                item for item in items 
                if search_lower in item["name"].lower() or search == str(item["category_id"])
            ]

        reverse = (sort_order.lower() == "desc")
        if sort_by == "id":
            items.sort(key=lambda x: x["category_id"], reverse=reverse)
        else:
            items.sort(key=lambda x: x["name"], reverse=reverse)

        return items[skip : skip + limit]

    async def get_by_id(self, category_id: int):
        result = await self.session.execute(select(Category).where(Category.category_id == category_id))
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    async def create(self, data: CategoryCreate):
        parent_id = None if data.parent_category_id == 0 else data.parent_category_id
        
        category_dict = data.model_dump()
        category_dict["parent_category_id"] = parent_id
        
        category = Category(**category_dict)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def update(self, category_id: int, data: CategoryUpdate):
        category = await self.get_by_id(category_id)
        update_data = data.model_dump(exclude_unset=True)
        
        if "parent_category_id" in update_data and update_data["parent_category_id"] == 0:
            update_data["parent_category_id"] = None
            
        for key, value in update_data.items():
            setattr(category, key, value)
            
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete(self, category_id: int):
        category = await self.get_by_id(category_id)
        await self.session.delete(category)
        await self.session.commit()