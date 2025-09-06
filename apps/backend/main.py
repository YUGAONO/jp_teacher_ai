from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

@router.post("/api/v1/examples")
async def get_examples(request: ExampleRequest):
    # モック応答 - 後でDify APIに置き換え
    mock_examples = {
        "N5": [
            f"{request.word}は毎日の習慣です。",
            f"私は図書館で{request.word}します。",
            f"友達と一緒に{request.word}するのが好きです。"
        ],
        "N4": [
            f"{request.word}することで、知識が増えます。",
            f"毎週末は{request.word}の時間です。",
            f"{request.word}の成果が見えてきました。"
        ],
        "N3": [
            f"{request.word}に励んでいる学生が多いです。",
            f"{request.word}の方法を工夫しています。",
            f"効率的な{request.word}が大切です。"
        ],
        "N2": [
            f"{request.word}に没頭するあまり、時間を忘れてしまいました。",
            f"計画的な{request.word}を心がけています。",
            f"{request.word}の成果が実を結びつつあります。"
        ],
        "N1": [
            f"徹底的な{request.word}によって、実力が著しく向上した。",
            f"{request.word}に関する効果的なアプローチを模索している。",
            f"継続的な{request.word}が、最終的に成功への鍵となる。"
        ]
    }
    
    return ExampleResponse(examples=mock_examples.get(request.level, []))

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/echo")
async def echo(request: EchoRequest):
    return {"message": request.text}

app.include_router(router)