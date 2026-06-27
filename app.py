"""
Streamlit chat UI for the IT Knowledge Base Assistant (RAG).

Run:  python -m streamlit run app.py
Works in mock mode out of the box; pick a provider in the sidebar for synthesized answers.
"""

import streamlit as st
from rag import load_documents, chunk_documents, build_index, respond

st.set_page_config(page_title="IT Knowledge Base Assistant", page_icon="📚", layout="centered")


@st.cache_resource
def get_index():
    chunks = chunk_documents(load_documents())
    return chunks, build_index(chunks)


st.title("📚 IT Knowledge Base Assistant")
st.caption("Ask a question and get an answer grounded in the IT documentation, with sources.")

provider = st.sidebar.selectbox("LLM provider", ["mock", "anthropic", "openai"], index=0)
k = st.sidebar.slider("Passages to retrieve (k)", 1, 6, 3)
st.sidebar.markdown("**mock** needs no API key and returns the retrieved passage.\n\n"
                    "**anthropic / openai** synthesize an answer from the retrieved context.")

chunks, index = get_index()
sources = sorted({c["source"] for c in chunks})
st.sidebar.markdown("**Knowledge base:**\n\n" + "\n".join(f"- {s}" for s in sources))

example = "I clicked a link in a suspicious email and typed my password. What should I do?"
query = st.text_input("Your question", value=example)

if st.button("Ask", type="primary") and query.strip():
    with st.spinner("Searching the knowledge base..."):
        result = respond(query, chunks, index, provider, k)
    st.markdown("### Answer")
    st.write(result["answer"])
    st.markdown("### Sources")
    if result["sources"]:
        for s in result["sources"]:
            st.markdown(f"- `{s['source']}`  (relevance {s['score']})")
    else:
        st.info("No relevant passages found in the knowledge base.")
