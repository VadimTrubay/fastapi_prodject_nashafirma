from sqlalchemy.orm import Session

from nashafirma_fastapi.database.models import Item, Order
from nashafirma_fastapi.schemas.items import InItem


async def get_item_by_id(item_id: int, db: Session):
    item = db.query(Item).filter_by(id=item_id).first()
    return item

async def get_items(order_id: int, limit: int, offset: int, db: Session):
    items = db.query(Item).filter(Item.order_id == order_id).limit(limit).offset(offset).all()
    return items

# async def get_item(item_id: int, db: Session):
#     item = await  get_item_by_id(item_id, db)
#     return item

async def create(body: InItem, db: Session):
    item = Item(**body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

async def update(item_id: int, body: InItem, db: Session):
    item = await  get_item_by_id(item_id, db)
    if item:
        item.order = body.order
        item.product = body.product
        item.weight = body.weight
        item.note = body.note
        db.commit()
    return item

async def remove(item_id: int, db: Session):
    item = await  get_item_by_id(item_id, db)
    if item:
        db.delete(item)
        db.commit()
    return item
