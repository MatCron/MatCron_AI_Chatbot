from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
import uuid

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def get_user_by_id(db: AsyncSession, user_id: str):

    result = await db.execute(select(User).filter(User.Id == user_id))
    return result.scalars().first()
