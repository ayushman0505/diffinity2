from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def build_chatbot(text):
    try:
        texts = [t for t in text.split("\n") if len(t.strip()) > 20]
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_texts(texts, embeddings)

        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            retriever=db.as_retriever()
        )
        return qa
    except:
        return None
