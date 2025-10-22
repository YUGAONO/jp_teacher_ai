from pydantic import BaseModel
from typing import List, Optional


class WordData(BaseModel):
    word: str
    hiragana: str
    rome: str
    synonyms: Optional[str] = ""
    antonym: Optional[str] = ""
    example: str
    example2: Optional[str] = ""
    example_rome: Optional[str] = ""
    example_rome2: Optional[str] = ""


class WordListRequest(BaseModel):
    words: List[str]  # 改行区切りの単語リスト


class PDFGenerateRequest(BaseModel):
    words_data: List[WordData]


class PDFResponse(BaseModel):
    success: bool
    pdf_base64: Optional[str] = None
    filename: Optional[str] = None
    size: Optional[int] = None
    word_count: Optional[int] = None
    error: Optional[str] = None
    message: Optional[str] = None