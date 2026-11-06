import asyncio
from sqlalchemy import select
from src.db.database import async_session_maker, engine
from src.models.category import Category
from src.models.product import Product, ProductCategory, ProductAttribute, ProductImage

async def seed_database():
    async with async_session_maker() as session:
        result = await session.execute(select(Category).limit(1))
        if result.scalars().first():
            print("База даних вже наповнена. Скасування...")
            return

        print("Створення категорій...")

        cat_root = Category(name="Для мотоцикліста", seo_keyword="moto", status=1)
        session.add(cat_root)
        await session.flush()

        cat_equip = Category(name="Екіпірування", parent_category_id=cat_root.category_id, status=1)
        cat_accs = Category(name="Аксесуари", parent_category_id=cat_root.category_id, status=1)
        session.add_all([cat_equip, cat_accs])
        await session.flush()

        cat_helmets = Category(name="Шоломи", parent_category_id=cat_equip.category_id, status=1)
        cat_backpacks = Category(name="Рюкзаки", parent_category_id=cat_accs.category_id, status=1)
        session.add_all([cat_helmets, cat_backpacks])
        await session.flush()

        print("Створення товарів...")

        product_helmet = Product(
            name="Шолом Shoei NXR2", 
            price=25500.0, 
            model="NXR2-Matt-Black", 
            description="Легкий спортивно-туристичний шолом",
            status=1
        )
        product_backpack = Product(
            name="Рюкзак Ogio No Drag Mach 5", 
            price=8500.0, 
            model="Mach-5", 
            description="Аеродинамічний жорсткий рюкзак",
            status=1
        )
        session.add_all([product_helmet, product_backpack])
        await session.flush()

        pc_helmet = ProductCategory(product_id=product_helmet.product_id, category_id=cat_helmets.category_id)
        pc_backpack = ProductCategory(product_id=product_backpack.product_id, category_id=cat_backpacks.category_id)
        session.add_all([pc_helmet, pc_backpack])

        attr1 = ProductAttribute(product_id=product_helmet.product_id, group_name="Характеристики", name="Розмір", value="M")
        attr2 = ProductAttribute(product_id=product_helmet.product_id, group_name="Характеристики", name="Колір", value="Чорний матовий")
        attr3 = ProductAttribute(product_id=product_backpack.product_id, group_name="Місткість", name="Об'єм", value="22 літри")
        session.add_all([attr1, attr2, attr3])

        img1 = ProductImage(product_id=product_helmet.product_id, image="https://motoprox.ua/upload/permanent-link/35/18590/detail/shlem-shoei-nxr2-black-gloss_00_big_500_500.webp", sort_order=1)
        img2 = ProductImage(product_id=product_backpack.product_id, image="https://images.prom.ua/7619728021_w640_h640_sumka-dlya-noutbuka.jpg", sort_order=1)
        session.add_all([img1, img2])

        await session.commit()
        print("База даних успішно наповнена тестовими даними!")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_database())