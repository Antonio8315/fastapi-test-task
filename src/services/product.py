from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from src.models.product import Product, ProductCategory, ProductAttribute, ProductImage
from src.schemas.product import ProductCreate

class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: int):
        result = await self.session.execute(select(Product).where(Product.product_id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def create(self, data: ProductCreate):
        product_dict = data.model_dump(exclude={"category_ids", "attributes", "images"})
        
        product = Product(**product_dict)
        self.session.add(product)
        await self.session.flush()

        for cat_id in data.category_ids:
            prod_cat = ProductCategory(product_id=product.product_id, category_id=cat_id)
            self.session.add(prod_cat)

        for attr in data.attributes:
            prod_attr = ProductAttribute(product_id=product.product_id, **attr.model_dump())
            self.session.add(prod_attr)

        for img in data.images:
            prod_img = ProductImage(product_id=product.product_id, **img.model_dump())
            self.session.add(prod_img)

        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product_id: int):
        product = await self.get_by_id(product_id)

        await self.session.delete(product)
        await self.session.commit()