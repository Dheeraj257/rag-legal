from loaders.folder_loader import process_folder
from retrieval.vector_store import build_bm25_store, build_vector_store
from api.utilities import reciprocal_rank_fusion
import json
from chains.rag_chain import eval_chain
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import pandas as pd


docs = process_folder("test_doc")
db = build_vector_store(docs)
bm25 = build_bm25_store(docs)

with open("golden_dataset.json", "r") as file:
    data = json.load(file)

questions = data["samples"]

all_results = []

for sample in questions:

    query = sample["question"]
    ground_truth = sample["ground_truth_answer"]

    db_result = db.similarity_search_with_score(query, k=6)
    bm25_result = bm25.invoke(query)
    result, score = reciprocal_rank_fusion(db_result, bm25_result, k=60)

    context = [content.page_content for content in result]
    context_string= "\n\n".join(context)
    final_result = eval_chain.invoke({"context":context_string, "question":query})

    result_dict = {
        "question": query,
        "answer": final_result,
        "contexts": context,
        "ground_truth": ground_truth
    }

    all_results.append(result_dict)

ragas_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
ragas_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

ragas_data = Dataset.from_list(all_results)
scores = evaluate(
    ragas_data, 
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm = ragas_llm,
    embeddings=ragas_embeddings)

df = scores.to_pandas()
df.to_csv("evaluation_score.csv",index=False)