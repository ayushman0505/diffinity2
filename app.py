import streamlit as st

from text_loader import load_document
from clause_engine import extract_clauses, classify_clause
from comparator import compare_documents
from risk_engine import calculate_risk
from summary_engine import generate_summary
from chatbot import build_chatbot

st.set_page_config(page_title="Diffinity", layout="wide")

st.title("⚖️ Diffinity — AI Document Comparator & Chatbot")
st.write("✅ App loaded successfully")

doc_type = st.selectbox(
    "Select Document Type",
    [
        "Legal Contract",
        "Academic / Research Paper",
        "Business / Policy Document",
        "General Document"
    ]
)

col1, col2 = st.columns(2)

with col1:
    doc1 = st.file_uploader("Upload Original Document", type=["pdf", "docx", "txt"])
with col2:
    doc2 = st.file_uploader("Upload Modified Document", type=["pdf", "docx", "txt"])

if doc1 and doc2:
    text1 = load_document(doc1)
    text2 = load_document(doc2)

    clauses1 = extract_clauses(text1)
    clauses2 = extract_clauses(text2)

    st.subheader("📑 Clause Comparison")

    results = compare_documents(clauses1, clauses2)

    if not results:
        st.warning("No comparable clauses found.")
    else:
        for r in results:
            if r["similarity"] < 0.85:
                clause_type = classify_clause(r["old_clause"])
                risk = (
                    calculate_risk(r["similarity"], clause_type)
                    if doc_type == "Legal Contract"
                    else None
                )

                title = f"⚠️ {clause_type.upper()} | Similarity: {r['similarity']}"
                if risk:
                    title += f" | Risk: {risk}"

                with st.expander(title):
                    st.markdown("**Original Clause**")
                    st.write(r["old_clause"])
                    st.markdown("**Modified Clause**")
                    st.write(r["new_clause"])
                    st.code(r["diff"])

    st.subheader("📝 Change Summary")
    for s in generate_summary(results):
        st.info(s)

    st.subheader("💬 AI Q&A Chatbot")
    qa = build_chatbot(text1 + "\n" + text2)

    if qa:
        question = st.text_input("Ask a question about the documents")
        if question:
            st.success(qa.run(question))
    else:
        st.info("Chatbot disabled (OpenAI API key not configured).")
