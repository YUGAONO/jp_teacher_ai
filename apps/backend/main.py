from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import os
import httpx
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Dify API configuration
API_KEY = os.getenv('DIFY_API_KEY', '')
BASE_URL = 'https://api.dify.ai/v1/workflows/run'

app = FastAPI()
SB = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

DUMMY_USER = "00000000-0000-0000-0000-000000000000"

origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "")
if origins_env.strip():
    allow_origins = [o.strip() for o in origins_env.split(",") if o.strip()]
else:
    allow_origins = ["http://localhost:8501", "http://127.0.0.1:8501"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router = APIRouter()

class EchoRequest(BaseModel):
    text: str

class ExampleRequest(BaseModel):
    word: str
    level: str

class ExampleResponse(BaseModel):
    examples: list[str]

async def get_dify_response(word: str, level: str) -> list[str]:
    """Get example sentences from Dify API"""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data: Dict[str, any] = {
        "inputs": {
            "word": word,
            "jlpt_level": level
        },
        "query": "",  # クエリはDify側で設定
        "response_mode": "blocking",
        "user": "example_generator",
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(BASE_URL, headers=headers, json=data)

            # Assuming the response contains newline-separated sentences
            response.raise_for_status()

            result = response.json()['data']['outputs']['結果']
            # Split the result into lines and filter out empty lines
            sentences = [line.strip() for line in result.split('\n') if line.strip()]
            return sentences
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/examples")
async def get_examples(request: ExampleRequest):
    # Keep mock examples as fallback
    mock_examples = {
        "5": [
            f"{request.word}は毎日の習慣です。",
            f"私は図書館で{request.word}します。",
            f"友達と一緒に{request.word}するのが好きです。"
        ],
        "4": [
            f"{request.word}することで、知識が増えます。",
            f"毎週末は{request.word}の時間です。",
            f"{request.word}の成果が見えてきました。"
        ],
        "3": [
            f"{request.word}に励んでいる学生が多いです。",
            f"{request.word}の方法を工夫しています。",
            f"効率的な{request.word}が大切です。"
        ],
        "2": [
            f"{request.word}に没頭するあまり、時間を忘れてしまいました。",
            f"計画的な{request.word}を心がけています。",
            f"{request.word}の成果が実を結びつつあります。"
        ],
        "1": [
            f"徹底的な{request.word}によって、実力が著しく向上した。",
            f"{request.word}に関する効果的なアプローチを模索している。",
            f"継続的な{request.word}が、最終的に成功への鍵となる。"
        ]
    }
    
    try:
        examples = []
        # if API_KEY:
        print(1111111111111)    
        #     # Use Dify API if API key is available
        #     examples = await get_dify_response(request.word, request.level)
        # else:
            
        #     # Fallback to mock examples if no API key
        #     examples = mock_examples.get(request.level, [])
        
        examples = mock_examples.get(request.level, [])
        # Save to Supabase
        data = {
            "user_id": DUMMY_USER,
            "input_word": request.word,
            "jlpt_level": request.level,
            "examples": examples
        }
        
        try:
            SB.table("example_sentences").insert(data).execute()
        except Exception as e:
            print(f"Failed to save to Supabase: {str(e)}")
            # Continue even if saving to database fails
            pass

        return ExampleResponse(examples=examples)
    except HTTPException as e:
        # Fallback to mock examples on API error
        examples = mock_examples.get(request.level, [])
        return ExampleResponse(examples=examples)

@app.get("/")
async def root():
    return {"message": "JLPT Example Generator API"}

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/echo")
async def echo(request: EchoRequest):
    return {"message": request.text}

app.include_router(router)