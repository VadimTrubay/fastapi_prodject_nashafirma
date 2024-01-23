from sqlalchemy.orm import Session

from nashafirma_fastapi.database.models import Order
from nashafirma_fastapi.schemas.orders import InOrder


async def get_order_by_id(order_id: int, db: Session):
    order = db.query(Order).filter_by(id=order_id).first()
    return order

async def get_orders(limit: int, offset: int, db: Session):
    orders = db.query(Order).order_by(Order.created_at).limit(limit).offset(offset).all()
    return orders

async def get_order(order_id: int, db: Session):
    order = await  get_order_by_id(order_id, db)
    return order

async def create(body: InOrder, db: Session):
    order = Order(**body.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

async def update(order_id: int, body: InOrder, db: Session):
    order = await  get_order_by_id(order_id, db)
    if order:
        order.done = body.done
        order.user = body.user
        db.commit()
    return order

async def remove(order_id: int, db: Session):
    order = await  get_order_by_id(order_id, db)
    if order:
        db.delete(order)
        db.commit()
    return order


def search_orders(db: Session, limit: int = 10, offset: int = 0, body: InOrder = None):
    query = db.query(Order)
    if body:
        if body.done:
            query = query.filter(Order.done.like(f"%{body.done}%"))
        if body.price:
            query = query.filter(Order.user.like(f"%{body.user}%"))

    orders = query.offset(offset).limit(limit).all()
    return orders