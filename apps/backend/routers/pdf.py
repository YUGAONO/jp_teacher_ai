from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.pdf import WordListRequest, PDFGenerateRequest, PDFResponse, WordData
from services.dify_client import get_word_analysis_from_dify
from services.pdf_service import pdf_service
from dependencies.auth import get_current_user

router = APIRouter(prefix="/pdf", tags=["PDF Generation"])


@router.post("/generate-from-words", response_model=PDFResponse)
async def generate_pdf_from_words(
    request: WordListRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    単語リストを受け取り、DifyでJSON分析してからPDFを生成する
    """
    print(f"PDF generation request received from user: {current_user}")
    print(f"Words count: {len(request.words)}")
    print(f"Words: {request.words}")
    
    try:
        if not request.words:
            raise HTTPException(status_code=400, detail="単語リストが空です")
        
        # Dify APIキーが有効な場合は実際のAPIを呼び出し、そうでなければモックデータを使用
        from config.settings import DIFY_API_KEY
        
        if DIFY_API_KEY and DIFY_API_KEY != "11111" and len(DIFY_API_KEY) > 10:
            print("Calling Dify API for word analysis...")
            try:
                word_analysis_data = await get_word_analysis_from_dify(request.words)
                print(f"Dify analysis completed. Data: {word_analysis_data}")
            except Exception as e:
                print(f"Dify API failed, using mock data instead: {str(e)}")
                # Dify APIが失敗した場合はモックデータを使用
                word_analysis_data = []
                for i, word in enumerate(request.words):
                    word_analysis_data.append({
                        'word': word,
                        'hiragana': f"{word}のひらがな",
                        'rome': f"word{i+1}",
                        'synonyms': f"{word}の類義語",
                        'antonym': f"{word}の反意語",
                        'example': f"{word}を使った例文です。",
                        'example_rome': f"{word} wo tsukatta reibun desu.",
                        'example2': f"{word}のもう一つの例文です。",
                        'example_rome2': f"{word} no mou hitotsu no reibun desu."
                    })
        else:
            print("Using mock data (Dify API key not configured)...")
            # モックデータを生成
            word_analysis_data = []
            for i, word in enumerate(request.words):
                word_analysis_data.append({
                    'word': word,
                    'hiragana': f"{word}のひらがな",
                    'rome': f"word{i+1}",
                    'synonyms': f"{word}の類義語",
                    'antonym': f"{word}の反意語",
                    'example': f"{word}を使った例文です。",
                    'example_rome': f"{word} wo tsukatta reibun desu.",
                    'example2': f"{word}のもう一つの例文です。",
                    'example_rome2': f"{word} no mou hitotsu no reibun desu."
                })
        
        print(f"Word analysis data prepared. Data: {word_analysis_data}")
        
        print("Generating PDF...")
        # PDF生成
        pdf_result = pdf_service.create_pdf_from_words(word_analysis_data)
        print(f"PDF generation result: {pdf_result.get('success', False)}")
        
        if not pdf_result['success']:
            print(f"PDF generation failed: {pdf_result.get('error')}")
            raise HTTPException(status_code=500, detail=pdf_result.get('error', 'PDF生成に失敗しました'))
        
        print("PDF generated successfully")
        return PDFResponse(**pdf_result)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in PDF generation: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"処理中にエラーが発生しました: {str(e)}")


@router.post("/generate-direct", response_model=PDFResponse)
async def generate_pdf_direct(
    request: PDFGenerateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    完成されたJSONデータを直接受け取ってPDFを生成する
    """
    try:
        if not request.words_data:
            raise HTTPException(status_code=400, detail="単語データが空です")
        
        # WordDataをdictに変換
        words_dict_list = [word.dict() for word in request.words_data]
        
        # PDF生成
        pdf_result = pdf_service.create_pdf_from_words(words_dict_list)
        
        if not pdf_result['success']:
            raise HTTPException(status_code=500, detail=pdf_result.get('error', 'PDF生成に失敗しました'))
        
        return PDFResponse(**pdf_result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"処理中にエラーが発生しました: {str(e)}")


@router.post("/generate-test", response_model=PDFResponse)
async def generate_test_pdf(
    request: WordListRequest
    # current_user: dict = Depends(get_current_user)  # 一時的に認証をスキップ
):
    """
    テスト用：Difyを使わずにモックデータでPDFを生成する
    """
    print(f"Test PDF generation request received")
    print(f"Words: {request.words}")
    
    try:
        if not request.words:
            raise HTTPException(status_code=400, detail="単語リストが空です")
        
        # モックデータを生成
        mock_data = []
        for i, word in enumerate(request.words):
            mock_data.append({
                'word': word,
                'hiragana': f"{word}のひらがな",
                'rome': f"word{i+1}",
                'synonyms': f"{word}の類義語",
                'antonym': f"{word}の反意語",
                'example': f"{word}を使った例文です。",
                'example_rome': f"{word} wo tsukatta reibun desu.",
                'example2': f"{word}のもう一つの例文です。",
                'example_rome2': f"{word} no mou hitotsu no reibun desu."
            })
        
        print(f"Generated mock data: {mock_data}")
        
        # PDF生成
        pdf_result = pdf_service.create_pdf_from_words(mock_data)
        print(f"PDF generation result: {pdf_result.get('success', False)}")
        
        if not pdf_result['success']:
            raise HTTPException(status_code=500, detail=pdf_result.get('error', 'PDF生成に失敗しました'))
        
        return PDFResponse(**pdf_result)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in test PDF generation: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"処理中にエラーが発生しました: {str(e)}")


@router.get("/health")
async def pdf_health_check():
    """PDF生成サービスのヘルスチェック"""
    try:
        # 簡単なテストデータでPDF生成をテスト
        test_data = [{
            'word': 'テスト',
            'hiragana': 'てすと',
            'rome': 'tesuto',
            'synonyms': '',
            'antonym': '',
            'example': 'これはテストです。',
            'example2': ''
        }]
        
        result = pdf_service.create_pdf_from_words(test_data)
        
        return {
            "status": "healthy" if result['success'] else "error",
            "message": "PDF generation service is working" if result['success'] else "PDF generation failed",
            "font_setup": pdf_service.setup_japanese_fonts()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Health check failed: {str(e)}"
        }