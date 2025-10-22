import { apiService } from './api'

// PDF関連の型定義
export interface WordData {
  word: string
  hiragana: string
  rome: string
  synonyms?: string
  antonym?: string
  example: string
  example2?: string
  example_rome?: string
  example_rome2?: string
}

export interface PDFResponse {
  success: boolean
  pdf_base64?: string
  filename?: string
  size?: number
  word_count?: number
  error?: string
  message?: string
}

export interface WordListRequest {
  words: string[]
}

export interface PDFGenerateRequest {
  words_data: WordData[]
}

export const pdfApi = {
  /**
   * 単語リストからPDFを生成
   */
  async generateFromWords(words: string[]): Promise<PDFResponse> {
    try {
      const response = await apiService.post<PDFResponse>('/pdf/generate-from-words', {
        words: words
      })
      return response.data
    } catch (error: any) {
      console.error('PDF generation error:', error)
      console.error('Error details:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        config: {
          url: error.config?.url,
          method: error.config?.method,
          baseURL: error.config?.baseURL
        }
      })
      throw error
    }
  },

  /**
   * 完成されたJSONデータから直接PDFを生成
   */
  async generateFromWordsData(wordsData: WordData[]): Promise<PDFResponse> {
    try {
      const response = await apiService.post<PDFResponse>('/pdf/generate-direct', {
        words_data: wordsData
      })
      return response.data
    } catch (error) {
      console.error('PDF generation error:', error)
      throw error
    }
  },

  /**
   * テスト用：モックデータでPDFを生成
   */
  async generateTestPDF(words: string[]): Promise<PDFResponse> {
    try {
      const response = await apiService.post<PDFResponse>('/pdf/generate-test', {
        words: words
      })
      return response.data
    } catch (error: any) {
      console.error('Test PDF generation error:', error)
      throw error
    }
  },

  /**
   * PDF生成サービスのヘルスチェック
   */
  async healthCheck(): Promise<any> {
    try {
      const response = await apiService.get<any>('/pdf/health')
      return response.data
    } catch (error) {
      console.error('PDF health check error:', error)
      throw error
    }
  }
}