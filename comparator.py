from sentence_transformers import SentenceTransformer, util
import difflib

def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def compare_documents(doc1_clauses, doc2_clauses):
    if not doc1_clauses or not doc2_clauses:
        return []

    model = get_model()
    emb1 = model.encode(doc1_clauses, convert_to_tensor=True)
    emb2 = model.encode(doc2_clauses, convert_to_tensor=True)

    results = []

    for i, c1 in enumerate(doc1_clauses):
        scores = util.cos_sim(emb1[i], emb2)[0]
        best_idx = scores.argmax().item()
        similarity = scores[best_idx].item()

        c2 = doc2_clauses[best_idx]

        diff = "\n".join(
            difflib.unified_diff(
                c1.split(),
                c2.split(),
                lineterm=""
            )
        )

        results.append({
            "old_clause": c1,
            "new_clause": c2,
            "similarity": round(similarity, 2),
            "diff": diff
        })

    return results
