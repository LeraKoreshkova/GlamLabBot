from aiogram import F, types, Router
from aiogram.filters import Command, or_f
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter
from handlers.processing import get_head_content
from kbds.inline import MenuCallBack
from kbds.reply import get_keyboard

user_router = Router()
user_router.message.filter(ChatTypeFilter(["private"]))


@user_router.message(Command('start', 'user'))
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_head_content(session=session, level=0, page_name="main")
    # await message.answer(" ", reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


# async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
#     user = callback.from_user
#     await orm_add_user(
#         session,
#         user_id=user.id,
#         first_name=user.first_name,
#         last_name=user.last_name,
#         phone=None,
#     )
#     await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
#     await callback.answer("Товар добавлен в корзину.")


@user_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):

    if callback_data.page_name == "add_to_cart":
        # await add_to_cart(callback, callback_data, session)
        return

    media, reply_markup = await get_head_content(
        session=session,
        level=callback_data.level,
        page_name=callback_data.page_name,
        category=callback_data.category,
        subcategory=callback_data.subcategory,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()



# @user_router.message(or_f(Command('catalog'), F.text.lower() == 'каталог'))
# async def catalog_cmd(message: types.Message):
#     await message.answer("Вот каталог:")
#
#
# @user_router.message(or_f(Command('about'), F.text.lower() == 'о магазине'))
# async def about_cmd(message: types.Message):
#     await message.answer("О нас:")
#
#
# @user_router.message(or_f(Command('payment'), F.text.lower() == 'варианты оплаты'))
# async def payment_cmd(message: types.Message):
#     await message.answer("Варианты оплаты:")
#
#
# @user_router.message(or_f(Command('shipping'), F.text.lower() == 'варианты доставки'))
# async def shipping_cmd(message: types.Message):
#     await message.answer("Варианты доставки:")