from pydantic import BaseModel

class EchoRequest(BaseModel):
    text: str

class ExampleRequest(BaseModel):
    word: str
    level: str

class ExampleResponse(BaseModel):
    examples: list[str]