from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from chains.prompt import prompt
from chains.memory import build_chain_with_memory
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

parser = StrOutputParser()

chain = prompt | llm | parser

chain_with_memory = build_chain_with_memory(chain)
