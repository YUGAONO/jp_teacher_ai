export interface ExampleRequest {
  word: string
  level: string
}

export interface ExampleResponse {
  examples: string[]
}

export interface EchoRequest {
  text: string
}