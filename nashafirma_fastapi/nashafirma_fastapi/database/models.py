from sqlalchemy import func, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String(100), unique=True, nullable=False)
    price = Column(Float(), default=0, nullable=True)
    created_at = Column(Date, default=func.current_date())
    updated_at = Column(Date, default=func.current_date(), onupdate=func.current_date())


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    done = Column(Boolean, default=False)
    user = Column(ForeignKey("users.id", ondelete="CASCADE"))
    user_id = relationship("User", backref="orders", lazy="joined")
    created_at = Column(Date, default=func.current_date())
    updated_at = Column(Date, default=func.current_date(), onupdate=func.current_date())


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=True, default=0.0)
    note = Column(String, nullable=True)
    order_id = Column(ForeignKey("orders.id", ondelete="CASCADE"))
    order = relationship("Order", backref="items", foreign_keys=[order_id])
    product_id = Column(ForeignKey("products.id", ondelete="CASCADE"))
    product = relationship("Product", backref="items", lazy="joined")
    created_at = Column(Date, default=func.current_date())
    updated_at = Column(Date, default=func.current_date(), onupdate=func.current_date())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    phone = Column(String(150), nullable=True)
    avatar = Column(String(350), nullable=True)
    confirmed = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    refresh_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    created_at = Column(Date, default=func.current_date())
    updated_at = Column(Date, default=func.current_date(), onupdate=func.current_date())
