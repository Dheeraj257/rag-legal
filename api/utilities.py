from chains.rag_chain import question_chain

def reciprocal_rank_fusion(vector_results, bm25_results, k=60):
    scores = {}
    content = {}

    for rank, (doc, score) in enumerate(vector_results):
        key = doc.page_content
        scores[key] = scores.get(key, 0) + 1/(rank + k)
        content[key] = doc

    for rank,doc in enumerate(bm25_results):
        key = doc.page_content
        scores[key] = scores.get(key, 0) + 1/(rank + k)
        content[key] = doc

    sorted_results = sorted(scores, key=lambda x:scores[x], reverse=True)
    result = [content[key] for key in sorted_results[:3]]
    best_score = min(score for doc, score in vector_results) if vector_results else 1.0

    return result, best_score

def normalize_query(history, user_query):

    previous = False
    reference = [ "previous", "that thing", "you mentioned", "we talked about", "the one", "tell me more"]

    if len(user_query.split()) < 10:
        previous = True
    elif any(query for query in user_query.split() if query) in ["it", "this", "that", "they", "those"]:
        previous = True
    for word in reference:
        if word in user_query:
            previous = True 

    last = history.messages[-2].content if len(history.messages) >= 2 else ""

    if previous == True:

        result = question_chain.invoke({"last":last, "user_query":user_query})
        print(f"Normalized query: {result}")
        return result   
    return user_query 