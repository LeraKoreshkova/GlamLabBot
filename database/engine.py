import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from common.text_for_db import categories, subcategories, description_for_info_pages
from database.models import Base
from database.orm_query import orm_create_categories, orm_create_subcategories, orm_add_banner_description

engine = create_async_engine(os.getenv('DB_PG'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        await orm_create_categories(session=session, categories=categories)
        for i in range(len(categories)):
            await orm_create_subcategories(session=session, subcategories=subcategories[i], category_id=i+1)
        await orm_add_banner_description(session=session, data=description_for_info_pages)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)