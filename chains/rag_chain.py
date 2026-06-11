from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from chains.prompt import prompt, question_prompt, guardrail_prompt, eval_prompt
from chains.memory import build_chain_with_memory
from dotenv import load_dotenv
from api.models import LLMGuardrailCheck

load_dotenv()

llm = ChatOpenAI()

llm_question = ChatOpenAI(model="gpt-4o-mini")

guardrail_model = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

chain = prompt | llm | parser

chain_with_memory = build_chain_with_memory(chain)

question_chain = question_prompt | llm_question | parser

structure_LLM_check = guardrail_model.with_structured_output(LLMGuardrailCheck)

guardrail_chain = guardrail_prompt | structure_LLM_check

eval_chain = eval_prompt | llm | parser
