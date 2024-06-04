from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_banner, orm_get_categories, orm_get_subcategories, orm_get_products
from kbds.inline import get_user_main_btns, get_user_catalog_btns, get_user_subcatalog_btns, get_products_btns
from utils.paginator import Paginator


async def main_page(*, session, level, page_name):
    banner = await orm_get_banner(session=session, page=page_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    kbds = get_user_main_btns(level=level)

    return image, kbds


async def catalog(*, session, level, page_name):
    banner = await orm_get_banner(session=session, page=page_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    categories = await orm_get_categories(session=session)
    kbds = get_user_catalog_btns(level=level, categories=categories)

    return image, kbds


async def subcatalog(*, session, level, category, page_name):
    banner = await orm_get_banner(session=session, page=page_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    subcategories = await orm_get_subcategories(session=session, category_id=category)
    kbds = get_user_subcatalog_btns(level=level, subcategories=subcategories)

    return image, kbds


def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns


async def products(*, session, level, subcategory, page):
    products = await orm_get_products(session=session, subcategory_id=subcategory)

    paginator = Paginator(products, page=page)
    product = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=product.image,
        caption=f"<strong>{product.name}\
                </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}\n\
                <strong>Товар {paginator.page} из {paginator.pages}</strong>",
    )

    pagination_btns = pages(paginator)

    kbds = get_products_btns(
        session=session,
        level=level,
        subcategory=subcategory,
        page=page,
        pagination_btns=pagination_btns,
        product_id=product.id,
    )

    return image, kbds


async def get_head_content(
    *,
    session: AsyncSession,
    level: int,
    page_name: str,
    category: int | None = None,
    subcategory: int | None = None,
    page: int | None = None,
    product_id: int | None = None,
    user_id: int | None = None
):
    if level == 0:
        return await main_page(session=session, level=level, page_name=page_name)
    elif level == 1:
        return await catalog(session=session, level=level, page_name=page_name)
    elif level == 2:
        return await subcatalog(session=session, level=level, category=category, page_name=page_name)
    elif level == 3:
        return await products(session=session, level=level, subcategory=subcategory, page=page)
    # elif level == 4:
    #     return await carts(session, level, page_name, page, user_id, product_id)