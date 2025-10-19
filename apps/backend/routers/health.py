from fastapi import APIRouter
from models.example import EchoRequest

router = APIRouter(tags=["health"])

@router.get("/")
async def root():
    return {"message": "JLPT Example Generator API"}

@router.get("/ping")
async def ping():
    return {"message": "pong"}

@router.post("/echo")
async def echo(request: EchoRequest):
    return {"message": request.text}