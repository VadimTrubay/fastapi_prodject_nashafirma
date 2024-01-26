from sqlalchemy.orm import Session

from nashafirma_fastapi.database.models import Order, User
from nashafirma_fastapi.schemas.orders import OrderModel, OrderCreate


async def get_order_by_id(order_id: int, db: Session):
    order = db.query(Order).filter_by(id=order_id).first()
    return order


async def get_orders_by_id_for_user(order_id: int, current_user: User, db: Session):
    order = db.query(Order).filter_by(id=order_id, user=current_user.id).first()
    return order


async def get_orders_by_user(limit: int, current_user: User, offset: int, db: Session):
    orders = db.query(Order).filter_by(user=current_user.id).limit(limit).offset(offset).all()
    return orders


async def get_orders_by_admin(limit: int, current_user: User, offset: int, db: Session):
    orders = db.query(Order).order_by(Order.created_at).limit(limit).offset(offset).all()
    if orders and current_user.is_superuser:
        return orders


async def create(body: OrderCreate, current_user: User, db: Session):
    order = Order(**body.model_dump())
    order.user = current_user.id
    if current_user.confirmed:
        db.add(order)
        db.commit()
        db.refresh(order)
    return order


async def update(order_id: int, current_user: User, body: OrderModel, db: Session):
    order = await  get_orders_by_id_for_user(order_id, current_user, db)
    if order:
        order.done = body.done
        db.commit()
    return order


async def remove(order_id: int, current_user: User, db: Session):
    order = await get_order_by_id(order_id, db)
    if order.user == current_user or current_user.is_superuser:
        db.delete(order)
        db.commit()
    return order


def search_orders(db: Session, current_user: User, limit: int = 10, offset: int = 0, query: str = None):
    if current_user.is_superuser:
        orders = (db.query(Order).
                  filter(Order.created_at.like(f"{query}")).
                  offset(offset).limit(limit).all())
        return orders
    if current_user.is_active:
        orders = (db.query(Order).
                  filter_by(user=current_user.id).
                  filter(Order.created_at == query).
                  offset(offset).limit(limit).all())
        return orders
