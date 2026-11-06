from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    parent_category_id: Mapped[int | None] = mapped_column(ForeignKey("category.category_id", ondelete="CASCADE"))
    seo_keyword: Mapped[str | None] = mapped_column(String(255))
    meta_title: Mapped[str | None] = mapped_column(String(255))
    meta_description: Mapped[str | None] = mapped_column(Text)
    meta_keyword: Mapped[str | None] = mapped_column(String(255))
    image: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[int] = mapped_column(Integer, default=1)
    date_added: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    date_modify: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    parent = relationship("Category", remote_side=[category_id], back_populates="subcategories")
    subcategories = relationship("Category", back_populates="parent", cascade="all, delete-orphan")