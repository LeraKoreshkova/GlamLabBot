from aiogram.utils.formatting import as_marked_section, Bold, as_list

categories = ['Обувь', 'Сумки', 'Головные уборы', 'Украшения', 'Пляж']
subcategories = [
    ['Кеды', 'Домашние тапочки', 'Сланцы', 'Кроссовки'],
    ['Рюкзаки', 'Сумки', 'Шопперы'],
    ['Шапки', 'Бейсболки', 'Панамки', 'Повязки на голову'],
    ['Серьги', 'Колье', 'Подвески', 'Кольца', 'Для волос', 'Ремни', 'Перчатки', 'Руковицы'],
    ['Закрытые купальники', 'Открытые купальники', 'Банданы','Платки']
]
colors = ['Красный', 'Розовый', 'Белый', 'Черный', '', '', '']


description_for_info_pages = {
    "main": "Добро пожаловать!",
    "about": "Магазин аксессуаров.\nРежим работы - круглосуточно.",
    "payment": as_marked_section(
        Bold("Варианты оплаты:"),
        "Картой в боте",
        "При получении карта/кеш",
        "В оффлайн магазине",
        marker="✅ ",
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
            Bold("Варианты доставки/заказа:"),
            "Курьер",
            "Самовынос",
            marker="✅ ",
        ),
        # as_marked_section(Bold("Нельзя:"), "Почта", "Голуби", marker="❌ "),
        # sep="\n----------------------\n",
    ).as_html(),
    'catalog': 'Категории:',
    'subcatalog': 'Подкатегории:',
    'cart': 'В корзине ничего нет!'
}