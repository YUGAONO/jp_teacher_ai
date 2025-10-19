from fastapi import APIRouter, Depends
from models.example import ExampleRequest, ExampleResponse
from services.example_service import generate_examples
from dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["examples"])

@router.post("/examples", response_model=ExampleResponse)
async def get_examples(request: ExampleRequest, current_user = Depends(get_current_user)):
    """例文を生成"""
    examples = await generate_examples(request.word, request.level, current_user.id)
    return ExampleResponse(examples=examples)