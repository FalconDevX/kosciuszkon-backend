from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.quiz import QuizQuestionResponse
from app.services.quiz_service import (
    get_all_questions_by_category,
    get_all_questions_by_difficulty,
    get_random_questions_by_category,
    get_random_questions_by_difficulty,
    get_random_questions,
)
    #test
router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"],
)


@router.get("/category/{category}", response_model=list[QuizQuestionResponse])
async def get_questions_category(
    category: str,
    db: AsyncSession = Depends(get_db),
):
    return await get_all_questions_by_category(db, category)


@router.get("/difficulty/{difficulty}", response_model=list[QuizQuestionResponse])
async def get_questions_difficulty(
    difficulty: str,
    db: AsyncSession = Depends(get_db),
):
    return await get_all_questions_by_difficulty(db, difficulty)


@router.get("/random/category/{category}", response_model=list[QuizQuestionResponse])
async def get_random_category_questions(
    category: str,
    db: AsyncSession = Depends(get_db),
):
    return await get_random_questions_by_category(db, category, 5)


@router.get("/random/difficulty/{difficulty}", response_model=list[QuizQuestionResponse])
async def get_random_difficulty_questions(
    difficulty: str,
    db: AsyncSession = Depends(get_db),
):
    return await get_random_questions_by_difficulty(db, difficulty, 5)


@router.get("/random", response_model=list[QuizQuestionResponse])
async def get_random_all_questions(
    db: AsyncSession = Depends(get_db),
):
    return await get_random_questions(db, 5)
