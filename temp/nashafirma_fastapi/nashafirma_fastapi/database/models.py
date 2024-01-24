from sqlalchemy import (func, Column, Integer, String, Float, Boolean, Enum)
import enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()


# class Role(enum.Enum):
#     admin: int = 1
#     user: int = 0


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
    user = Column(ForeignKey('users.id', ondelete='CASCADE'))
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


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    # roles = Column('roles', Enum(Role), default=Role.user)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    phone = Column(String(150), nullable=True)
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    user = Column(ForeignKey('users.id', ondelete='CASCADE'))
    user_id = relationship('User', backref="profiles", lazy='joined')
