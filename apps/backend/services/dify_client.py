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


async def get_word_analysis_from_dify(words_list: List[str]) -> List[Dict]:
    """Get word analysis from Dify API for PDF generation"""
    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # 単語リストを改行区切りの文字列に変換
    words_text = "\n".join(words_list)
    
    data: Dict[str, any] = {
        "inputs": {
            "words_list": words_text
        },
        "query": "",  # クエリはDify側で設定
        "response_mode": "blocking",
        "user": "pdf_generator",
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            print(f"Dify API Request: URL={DIFY_BASE_URL}")
            print(f"Dify API Request: Headers={headers}")
            print(f"Dify API Request: Data={data}")
            
            response = await client.post(DIFY_BASE_URL, headers=headers, json=data)
            
            print(f"Dify API Response: Status={response.status_code}")
            print(f"Dify API Response: Headers={dict(response.headers)}")
            
            if response.status_code != 200:
                response_text = response.text
                print(f"Dify API Error Response: {response_text}")
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"Dify API returned {response.status_code}: {response_text}"
                )
            
            response_json = response.json()
            print(f"Dify API Response JSON: {response_json}")
            
            # レスポンス構造をチェック
            if 'data' not in response_json:
                raise HTTPException(status_code=500, detail=f"Invalid response structure: 'data' field missing. Response: {response_json}")
            
            if 'outputs' not in response_json['data']:
                raise HTTPException(status_code=500, detail=f"Invalid response structure: 'outputs' field missing. Response: {response_json}")
            
            if 'word_analysis' not in response_json['data']['outputs']:
                raise HTTPException(status_code=500, detail=f"Invalid response structure: 'word_analysis' field missing. Available fields: {list(response_json['data']['outputs'].keys())}")
            
            result = response_json['data']['outputs']['word_analysis']
            print(f"Word analysis result: {result}")
            print(f"Word analysis result type: {type(result)}")
            
            # Difyからリスト形式で返される場合とJSON文字列で返される場合の両方に対応
            if isinstance(result, list):
                # すでにリスト形式の場合はそのまま返す
                print("Result is already a list, returning as-is")
                return result
            elif isinstance(result, str):
                # JSON文字列の場合はパースする
                print("Result is a string, attempting to parse as JSON")
                import json
                try:
                    word_data_list = json.loads(result)
                    return word_data_list
                except json.JSONDecodeError as json_err:
                    raise HTTPException(status_code=500, detail=f"Invalid JSON in word_analysis field: {str(json_err)}. Raw content: {result}")
            else:
                # その他の形式の場合はエラー
                raise HTTPException(status_code=500, detail=f"Unexpected data type for word_analysis: {type(result)}. Content: {result}")
                
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Dify API request timed out")
        except httpx.RequestError as req_err:
            raise HTTPException(status_code=503, detail=f"Dify API connection error: {str(req_err)}")
        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected Dify API error: {str(e)}")