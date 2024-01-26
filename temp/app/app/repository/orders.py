from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.app_db import get_db
from app.database.models import Order
from app.schemas.orders import InOrder


async def get_order_by_id(order_id: int, db: AsyncSession = Depends(get_db)):
    order = db.query(Order).filter_by(id=order_id).first()
    return order

async def get_orders(limit: int, offset: int, db: AsyncSession = Depends(get_db)):
    orders = db.query(Order).order_by(Order.created_at).limit(limit).offset(offset).all()
    return orders

async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await  get_order_by_id(order_id, db)
    return order

async def create(body: InOrder, db: AsyncSession = Depends(get_db)):
    order = Order(**body.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

async def update(order_id: int, body: InOrder, db: AsyncSession = Depends(get_db)):
    order = await  get_order_by_id(order_id, db)
    if order:
        order.done = body.done
        order.user = body.user
        db.commit()
    return order

async def remove(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await  get_order_by_id(order_id, db)
    if order:
        db.delete(order)
        db.commit()
    return order


def search_orders(db: AsyncSession = Depends(get_db), limit: int = 10, offset: int = 0, body: InOrder = None):
    query = db.query(Order)
    if body:
        if body.done:
            query = query.filter(Order.done.like(f"%{body.done}%"))
        if body.price:
            query = query.filter(Order.user.like(f"%{body.user}%"))

    orders = query.offset(offset).limit(limit).all()
    return orders