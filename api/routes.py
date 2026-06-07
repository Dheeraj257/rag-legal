from fastapi import APIRouter
from api.models import Question
from chains.memory import get_session_history
from chains.rag_chain import chain_with_memory
from retrieval.db import get_db, get_bm25
from api.guardrail_check import check_guardrail
from api.utilities import normalize_query, reciprocal_rank_fusion
    
    
router = APIRouter()

@router.post("/ask")
def ask(body: Question):

    session_id = body.session_id
    check = check_guardrail(body.text)
    if not check.passed:
        return {
            "question": body.text,
            "answer": "Your question cannot be processed",
            "session_id": body.session_id,
            "citations": [],
            "guardrail_fail": True,
            "reason": check.reason,
            }
    history = get_session_history(session_id)
    db = get_db()
    bm25 = get_bm25()
    
    if history.messages:
        search_query = normalize_query(history, body.text)
    else:
        search_query = body.text


    db_retriever = db.as_retriever(search_kwargs={"k": 6})
    vector_results = db_retriever.invoke(search_query)
    bm25_results = bm25.invoke(search_query)
    results = reciprocal_rank_fusion(vector_results, bm25_results,k=60)

    context_list = []
    citations = []
    for content in results:
        location = "unknown"
        source = content.metadata.get("source","unknown")
        if "page" in content.metadata:
            location = content.metadata.get("page", "unknown")
        if "row" in content.metadata:
            location = content.metadata.get("row","unknown")
        citation = f"{source} - {location}"
        citations.append({"source":source, "location":location})
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
        "session_id": body.session_id,
        "citations": citations
    }

