from api.models import LLMGuardrailCheck
from chains.rag_chain import guardrail_chain

def check_guardrail(query):

    if not query.strip():
        return LLMGuardrailCheck(
            harmful_content=True,
            prompt_injection=True,
            relevance_check=True , 
            reason="No question available",
            passed=False)
    elif len(query.split()) > 1000:
        return LLMGuardrailCheck(
            harmful_content=True,
            prompt_injection=True,
            relevance_check=True , 
            reason="The question needs to less than 1000 words",
            passed=False
        )
    result = guardrail_chain.invoke({"user_query":query})
    return result