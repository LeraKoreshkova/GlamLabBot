from sqlalchemy import String, ForeignKey, Text, Numeric, DateTime, func, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    pass


class Banner(Base):
    __tablename__ = 'banners'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    image: Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)


class Subcategory(Base):

    __tablename__ = 'subcategories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
#     category: Mapped['Category'] = relationship(backref='subcategories')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('subcategories.id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(8,2), nullable=False)
    image: Mapped[str] = mapped_column(String(200), nullable=False)
    # color: Mapped[str | None] = None
    # size: Mapped[str | None] = None

    # subcategory: Mapped['Subcategory'] = relationship(backref='products')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[int]

    # user: Mapped['User'] = relationship(backref='cart')
    # product: Mapped['Product'] = relationship(backref='cart')


class Color(Base):
    __tablename__ = 'colors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    color: Mapped[str] = mapped_column(String(200), nullable=False)



class ProductColor(Base):
    __tablename__ = 'productscolors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    color_id: Mapped[int] = mapped_column(ForeignKey('colors.id', ondelete='CASCADE'))


# class Size(Base):
#     ...

# class Color(Base):
#     __tablename__ = 'colors'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     color: Mapped[str] = mapped_column(String(200), nullable=False)
#
#
# class ProductColor(Base):
#     __tablename__ = 'productscolors'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
#     color_id: Mapped[int] = mapped_column(ForeignKey('colors.id', ondelete='CASCADE'))
