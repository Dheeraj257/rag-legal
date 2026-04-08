from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system","""You are a helpful document assistant.
Use the context below to answer the question as completely as possible.
Combine information from multiple parts of the context if needed.
If the context contains partial information — use what is available and say so.
Only say 'Not found in documents' if the context has absolutely no relevant information.

Each chunk ends with [Source: ...] — include the source in your answer.

Context:
{context}"""),
MessagesPlaceholder("history"),
 ("human","{question}") ])