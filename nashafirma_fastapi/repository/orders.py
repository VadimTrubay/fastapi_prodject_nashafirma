from nashafirma_fastapi.database.models import Order, User
from nashafirma_fastapi.schemas.orders import OrderModel, OrderCreate
from sqlalchemy import Text, cast, or_
from sqlalchemy.orm import Session


async def get_order_by_id(current_user: User, order_id: int, db: Session):
    if current_user.is_superuser:
        order = db.query(Order).filter_by(id=order_id).first()
    else:
        order = db.query(Order).filter_by(id=order_id, user=current_user.id).first()
    return order


async def get_orders(limit: int, current_user: User, offset: int, db: Session):
    if current_user.is_superuser:
        orders = db.query(Order).order_by(Order.created_at).limit(limit).offset(offset).all()
    else:
        orders = db.query(Order).order_by(Order.created_at).filter_by(user=current_user.id).limit(limit).offset(
            offset).all()
    return orders


async def create(body: OrderCreate, current_user: User, db: Session):
    order = Order(**body.model_dump())
    order.user_id = current_user.id
    if current_user.confirmed:
        db.add(order)
        db.commit()
        db.refresh(order)
    return order


async def update(order_id: int, current_user: User, body: OrderModel, db: Session):
    if current_user.is_superuser:
        order = await get_order_by_id(current_user, order_id, db)
        if order:
            order.done = body.done
            db.commit()
    else:
        order = await get_order_by_id(current_user, order_id, db)
        if order:
            order.done = body.done
            db.commit()
    return order


async def remove(order_id: int, current_user: User, db: Session):
    order = await get_order_by_id(current_user, order_id, db)
    if order.user == current_user or current_user.is_superuser:
        db.delete(order)
        db.commit()
    return order


def search_orders(db: Session, current_user: User, limit: int = 10, offset: int = 0, query: str = None):
    if current_user.is_superuser:
        if query:
            orders = (
                db.query(Order)
                .filter(
                    or_(
                        # cast(Order.user, Text).ilike(f"%{query}%"),
                        cast(Order.created_at, Text).ilike(f"%{query}%"),
                    )
                )
                .limit(limit)
                .offset(offset)
                .all()
            )
            return orders

    if current_user.is_confirmed:
        if query:
            orders = (
                db.query(Order)
                .filter(
                    or_(
                        # cast(Order.user, Text).ilike(f"%{query}%"),
                        cast(Order.created_at, Text).ilike(f"%{query}%"),
                    )
                )
                .limit(limit)
                .offset(offset)
                .all()
            )
            return orders
