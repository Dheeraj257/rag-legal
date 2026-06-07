from pydantic import BaseModel

class Question(BaseModel):

    text: str
    session_id: str

class LLMGuardrailCheck(BaseModel):

      harmful_content: bool
      prompt_injection: bool
      relevance_check: bool 
      reason: str
      passed: bool