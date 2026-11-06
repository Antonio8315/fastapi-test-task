from datetime import datetime
from sqlalchemy import String, Text, Integer, Float, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    seo_keyword: Mapped[str | None] = mapped_column(String(255))
    meta_title: Mapped[str | None] = mapped_column(String(255))
    meta_description: Mapped[str | None] = mapped_column(Text)
    meta_keyword: Mapped[str | None] = mapped_column(String(255))
    image: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[int] = mapped_column(Integer, default=1)
    date_added: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    date_modify: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    price: Mapped[float] = mapped_column(Float, default=0.0)
    model: Mapped[str | None] = mapped_column(String(255))
    manufacturer_id: Mapped[int | None] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    viewed: Mapped[int] = mapped_column(Integer, default=0)

    categories = relationship("ProductCategory", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    attributes = relationship("ProductAttribute", back_populates="product", cascade="all, delete-orphan")

class ProductCategory(Base):
    __tablename__ = "product_category"
    __table_args__ = (UniqueConstraint('product_id', 'category_id', name='uix_product_category'),)

    product_category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id", ondelete="CASCADE"))

    product = relationship("Product", back_populates="categories")

class ProductImage(Base):
    __tablename__ = "product_image"

    product_image_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id", ondelete="CASCADE"))
    image: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    product = relationship("Product", back_populates="images")

class ProductAttribute(Base):
    __tablename__ = "product_attribute"

    product_attribute_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id", ondelete="CASCADE"))
    group_name: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    product = relationship("Product", back_populates="attributes")