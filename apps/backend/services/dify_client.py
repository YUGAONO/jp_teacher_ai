import httpx
from fastapi import HTTPException
from typing import Dict, List
from config.settings import DIFY_API_KEY, DIFY_BASE_URL

async def get_dify_response(word: str, level: str) -> List[str]:
    """Get example sentences from Dify API"""
    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
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
            response = await client.post(DIFY_BASE_URL, headers=headers, json=data)

            # Assuming the response contains newline-separated sentences
            response.raise_for_status()

            result = response.json()['data']['outputs']['結果']
            # Split the result into lines and filter out empty lines
            sentences = [line.strip() for line in result.split('\n') if line.strip()]
            return sentences
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))