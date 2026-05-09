from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from app.models import QuizQuestion


async def get_all_questions_by_category(
    db: AsyncSession,
    category: str,
):
    result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.category == category)
    )
    return result.scalars().all()


async def get_all_questions_by_difficulty(
    db: AsyncSession,
    difficulty: str,
):
    result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.difficulty == difficulty)
    )
    return result.scalars().all()


async def get_random_questions_by_category(
    db: AsyncSession,
    category: str,
    limit: int = 5,
):
    result = await db.execute(
        select(QuizQuestion)
        .where(QuizQuestion.category == category)
        .order_by(func.random())
        .limit(limit)
    )
    return result.scalars().all()


async def get_random_questions_by_difficulty(
    db: AsyncSession,
    difficulty: str,
    limit: int = 5,
):
    result = await db.execute(
        select(QuizQuestion)
        .where(QuizQuestion.difficulty == difficulty)
        .order_by(func.random())
        .limit(limit)
    )
    return result.scalars().all()


async def get_random_questions(
    db: AsyncSession,
    limit: int = 5,
):
    result = await db.execute(
        select(QuizQuestion)
        .order_by(func.random())
        .limit(limit)
    )
    return result.scalars().all()
