import { apiService } from './api'
import type { ExampleRequest, ExampleResponse } from '@/types'

export class ExampleService {
  async generateExamples(request: ExampleRequest): Promise<ExampleResponse> {
    const response = await apiService.post<ExampleResponse>('/api/v1/examples', request)
    return response.data
  }
}

export const exampleService = new ExampleService()