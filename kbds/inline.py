import asyncio
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_subcategory


class MenuCallBack(CallbackData, prefix="page"):
    level: int
    page_name: str
    category: int | None = None
    subcategory: int | None = None
    page: int = 1
    product_id: int | None = None


def get_user_main_btns(*, level: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Товары 🛍️": "catalog",
        "Корзина 🛒": "cart",
        "О нас ℹ️": "about",
        "Оплата 💵": "payment",
        "Доставка ✈️": "shipping",
    }
    for text, page_name in btns.items():
        if page_name == 'catalog':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1, page_name=page_name).pack()))
        elif page_name == 'cart':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=4, page_name=page_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level, page_name=page_name).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_catalog_btns(*, level: int, categories: list, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level=level - 1, page_name='main').pack()))
    keyboard.add(InlineKeyboardButton(text='Корзина 🛒',
                                      callback_data=MenuCallBack(level=4, page_name='cart').pack()))

    for obj in categories:
        keyboard.add(InlineKeyboardButton(text=obj.name,
                                          callback_data=MenuCallBack(level=level + 1, page_name='subcatalog',
                                                                     category=obj.id).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_subcatalog_btns(*, level: int, subcategories: list, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level=level - 1, page_name='catalog').pack()))
    keyboard.add(InlineKeyboardButton(text='Корзина 🛒',
                                      callback_data=MenuCallBack(level=4, page_name='cart').pack()))

    for obj in subcategories:
        keyboard.add(InlineKeyboardButton(text=obj.name,
                                          callback_data=MenuCallBack(level=level + 1, page_name=obj.name,
                                                                     subcategory=obj.id).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_products_btns(
        *,
        session: AsyncSession,
        level: int,
        subcategory: int,
        page: int,
        pagination_btns: dict,
        product_id: int,
        sizes: tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()

    # subcategory_id = orm_get_subcategory(session=session, product_id=product_id)

    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level=level - 1, page_name='subcatalog', subcategory=subcategory).pack()))
    keyboard.add(InlineKeyboardButton(text='Корзина 🛒',
                                      callback_data=MenuCallBack(level=4, page_name='cart').pack()))
    keyboard.add(InlineKeyboardButton(text='Купить 💵',
                                      callback_data=MenuCallBack(level=level, page_name='add_to_cart',
                                                                 product_id=product_id).pack()))

    keyboard.adjust(*sizes)

    row = []
    for text, page_name in pagination_btns.items():
        if page_name == "next":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level=level,
                                                page_name=page_name,
                                                subcategory=subcategory,
                                                page=page + 1).pack()))

        elif page_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level=level,
                                                page_name=page_name,
                                                subcategory=subcategory,
                                                page=page - 1).pack()))

    return keyboard.row(*row).as_markup()


def get_user_cart(
        *,
        level: int,
        page: int | None,
        pagination_btns: dict | None,
        product_id: int | None,
        sizes: tuple[int] = (3,)
):
    keyboard = InlineKeyboardBuilder()
    if page:
        keyboard.add(InlineKeyboardButton(text='Удалить',
                                          callback_data=MenuCallBack(level=level, menu_name='delete',
                                                                     product_id=product_id, page=page).pack()))
        keyboard.add(InlineKeyboardButton(text='-1',
                                          callback_data=MenuCallBack(level=level, menu_name='decrement',
                                                                     product_id=product_id, page=page).pack()))
        keyboard.add(InlineKeyboardButton(text='+1',
                                          callback_data=MenuCallBack(level=level, menu_name='increment',
                                                                     product_id=product_id, page=page).pack()))

        keyboard.adjust(*sizes)

        row = []
        for text, menu_name in pagination_btns.items():
            if menu_name == "next":
                row.append(InlineKeyboardButton(text=text,
                                                callback_data=MenuCallBack(level=level, menu_name=menu_name,
                                                                           page=page + 1).pack()))
            elif menu_name == "previous":
                row.append(InlineKeyboardButton(text=text,
                                                callback_data=MenuCallBack(level=level, menu_name=menu_name,
                                                                           page=page - 1).pack()))

        keyboard.row(*row)

        row2 = [
            InlineKeyboardButton(text='На главную 🏠',
                                 callback_data=MenuCallBack(level=0, menu_name='main').pack()),
            InlineKeyboardButton(text='Заказать',
                                 callback_data=MenuCallBack(level=0, menu_name='order').pack()),
        ]
        return keyboard.row(*row2).as_markup()
    else:
        keyboard.add(
            InlineKeyboardButton(text='На главную 🏠',
                                 callback_data=MenuCallBack(level=0, menu_name='main').pack()))

        return keyboard.adjust(*sizes).as_markup()


def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()
