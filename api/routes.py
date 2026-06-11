from fastapi import APIRouter, Depends
from api.models import Question
from chains.memory import get_session_history
from chains.rag_chain import chain_with_memory
from retrieval.db import get_db, get_bm25
from api.guardrail_check import check_guardrail
from api.utilities import normalize_query, reciprocal_rank_fusion
    
    
router = APIRouter()

@router.post("/ask")
def ask(body: Question, db=Depends(get_db), bm25=Depends(get_bm25)):

    session_id = body.session_id
    check = check_guardrail(body.text)
    if not check.passed:
        return {
            "question": body.text,
            "answer": "Your question cannot be processed",
            "session_id": body.session_id,
            "citations": [],
            "guardrail_failed": True,
            "reason": check.reason,
            }
    history = get_session_history(session_id)
    
    if history.messages:
        search_query = normalize_query(history, body.text)
    else:
        search_query = body.text


    vector_results = db.similarity_search_with_score(search_query, k=6)
    bm25_results = bm25.invoke(search_query)
    results, best_score = reciprocal_rank_fusion(vector_results, bm25_results,k=60)

    if best_score > 0.7:
        return {
             "question": body.text,
            "answer": "I don't have sufficient information in the provided documents to answer this.",
            "session_id": body.session_id,
            "citations": [],
            "guardrail_failed": False,
            "reason": "Low retrieval confidence",
        }

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

