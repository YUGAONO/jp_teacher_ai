from typing import List
from fastapi import HTTPException
from database.supabase import SB
from services.dify_client import get_dify_response
from config.settings import DIFY_API_KEY

async def generate_examples(word: str, level: str, user_id: str) -> List[str]:
    """例文を生成し、データベースに保存"""
    
    # Mock examples as fallback
    mock_examples = {
        "5": [
            f"{word}は毎日の習慣です。",
            f"私は図書館で{word}します。",
            f"友達と一緒に{word}するのが好きです。"
        ],
        "4": [
            f"{word}することで、知識が増えます。",
            f"毎週末は{word}の時間です。",
            f"{word}の成果が見えてきました。"
        ],
        "3": [
            f"{word}に励んでいる学生が多いです。",
            f"{word}の方法を工夫しています。",
            f"効率的な{word}が大切です。"
        ],
        "2": [
            f"{word}に没頭するあまり、時間を忘れてしまいました。",
            f"計画的な{word}を心がけています。",
            f"{word}の成果が実を結びつつあります。"
        ],
        "1": [
            f"徹底的な{word}によって、実力が著しく向上した。",
            f"{word}に関する効果的なアプローチを模索している。",
            f"継続的な{word}が、最終的に成功への鍵となる。"
        ]
    }
    
    try:
        examples = []
        # if DIFY_API_KEY:
        print(f"User {user_id} requested examples for word: {word}")    
        #     # Use Dify API if API key is available
        #     examples = await get_dify_response(word, level)
        # else:
        #     # Fallback to mock examples if no API key
        #     examples = mock_examples.get(level, [])
        
        examples = mock_examples.get(level, [])
        
        # Save to Supabase with actual user ID
        data = {
            "user_id": user_id,
            "input_word": word,
            "jlpt_level": level,
            "examples": examples
        }
        
        try:
            SB.table("example_sentences").insert(data).execute()
        except Exception as e:
            print(f"Failed to save to Supabase: {str(e)}")
            # Continue even if saving to database fails
            pass

        return examples
    except HTTPException as e:
        # Fallback to mock examples on API error
        examples = mock_examples.get(level, [])
        return examples