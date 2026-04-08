from fastapi import APIRouter
from api.models import Question
from chains.memory import get_session_history
from chains.rag_chain import chain_with_memory
from retrieval.db import get_db


router = APIRouter()

@router.post("/ask")
def ask(body: Question):

    session_id = body.session_id
    history = get_session_history(session_id)
    db = get_db()
    
    if history.messages:
        last = history.messages[-2].content if len(history.messages) >= 2 else ""
        search_query = f"{last} + {body.text}"
    else:
        search_query = body.text


    retriever = db.as_retriever(search_kwargs={"k":3})
    results = retriever.invoke(search_query)

    context_list = []
    for content in results:
        citation = content.metadata.get("citation","unknown")
        context_list.append(f"{content.page_content}:\n\n{citation}")
    context = "\n\n".join(context_list)

    config = {"configurable":{"session_id": body.session_id}}

    answer = chain_with_memory.invoke({
        "context":context,
        "question":body.text
    }, config=config)

    return {
        "question": body.text,
        "answer": answer,
        "session_id": body.session_id
    }

