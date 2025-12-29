import spacy

def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except:
        return None

nlp = load_nlp()

CLAUSE_KEYWORDS = {
    "liability": ["liability", "damages", "indemnity"],
    "termination": ["termination", "terminate", "cancel"],
    "payment": ["payment", "fee", "compensation"],
    "confidentiality": ["confidential", "nda"],
}

def extract_clauses(text):
    if not nlp or not text:
        return []

    clauses = []
    doc = nlp(text)
    for sent in doc.sents:
        if len(sent.text.strip()) > 40:
            clauses.append(sent.text.strip())
    return clauses

def classify_clause(clause):
    clause = clause.lower()
    for k, v in CLAUSE_KEYWORDS.items():
        if any(word in clause for word in v):
            return k
    return "general"
