from sqlalchemy import (func, Column, Integer, String, Float, Boolean, Enum)
import enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

from nashafirma_fastapi.database.db import engine

Base = declarative_base()

class Role(enum.Enum):
    admin: str = 'admin'
    user: str = 'user'


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String(100), unique=True, nullable=False)
    price = Column(Float(), default=0, nullable=True)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column('created_at', DateTime, default=func.now())
    done = Column(Boolean, default=False)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'))


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=True, default=0)
    note = Column(String, nullable=True)

    order_id = Column(ForeignKey('orders.id', ondelete='CASCADE'))
    order = relationship('Order', backref="items", foreign_keys=[order_id])

    product_id = Column(ForeignKey('products.id', ondelete='CASCADE'))
    product = relationship('Product', backref="items", foreign_keys=[product_id])


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    phone = Column(String(150), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    roles = Column('roles', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    api_key = Column(String(100), nullable=True)

Base.metadata.create_all(engine)
Base.metadata.bind = engine
