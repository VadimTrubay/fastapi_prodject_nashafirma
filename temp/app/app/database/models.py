from sqlalchemy import (ForeignKey, func, Column, Integer, String, Float, Boolean)
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import DeclarativeBase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, generics
import enum
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import DeclarativeBase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, generics



class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String(100), unique=True, nullable=False)
    price = Column(Float(), default=0, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    done = Column(Boolean, default=False)
    user = Column(generics.GUID(), ForeignKey('user.id', ondelete='CASCADE'))
    user_id = relationship('User', backref="orders", lazy='joined')


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=True, default=0.0)
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    order_id = Column(ForeignKey('orders.id', ondelete='CASCADE'))
    order = relationship('Order', backref="items", foreign_keys=[order_id])
    product_id = Column(ForeignKey('products.id', ondelete='CASCADE'))
    product = relationship('Product', backref="items", lazy='joined')


class User(SQLAlchemyBaseUserTableUUID, Base):
    user_name: Mapped[str] = mapped_column(String(50), nullable=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    avatar: Mapped[str] = mapped_column(String(150), nullable=True)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())

