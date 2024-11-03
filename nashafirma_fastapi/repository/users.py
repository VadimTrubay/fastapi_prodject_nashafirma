from nashafirma_fastapi.database.models import User
from nashafirma_fastapi.schemas.users import UserModel, UserUpdate
from sqlalchemy.orm import Session


async def get_user_by_id(user_id: int, db: Session) -> User | None:
    user = db.query(User).filter_by(id=user_id).first()
    return user


async def get_user_by_email(email: str, db: Session) -> User | None:
    user = db.query(User).filter_by(email=email).first()
    return user


async def get_me(current_user: User, db: Session) -> User | None:
    user = db.query(User).filter_by(email=current_user.email).first()
    return user


async def create_user(body: UserModel, db: Session):
    new_user = User(**body.model_dump())
    if len(db.query(User).all()) == 0:  # First user always admin
        new_user.is_superuser = True
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update(current_user: User, body: UserUpdate, db: Session):
    user = db.query(User).filter_by(email=current_user.email).first()
    if user:
        user.username = body.username
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.phone = body.phone
        db.commit()
    return user


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def remove(user_id: int, db: Session) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
