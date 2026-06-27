"""
IT Knowledge Base Assistant (RAG)
---------------------------------
A lightweight Retrieval-Augmented Generation app: ask natural-language questions
over a folder of IT documents and get answers grounded in those docs, with sources.

Design goals:
  - Runs with ZERO setup (no API key, no heavy deps): a pure-Python TF-IDF retriever
    plus an extractive "mock" answer.
  - Upgrades to full RAG with one env var: retrieved context is sent to an LLM
    (Claude or OpenAI) that answers using only that context and cites sources.

Modes (LLM_PROVIDER): mock (default) | anthropic | openai

Usage:
  python rag.py "How do I reset my password?"
  python rag.py "What do I need to onboard a new hire?" --provider anthropic --k 4
  python rag.py "Is this email a phishing attempt?" --pretty

Author: Roger Perez
License: MIT
"""

import argparse
import glob
import json
import math
import os
import re
import sys
from collections import Counter

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

DOCS_DIR = os.getenv("KB_DOCS_DIR", "docs")

STOPWORDS = set((
    "a an the of to and or in on for with is are was were be been being do does did "
    "this that these those it its as at by from into your you i we they he she them "
    "if then else when while how what which who whom where why can could should would "
    "will shall may might must not no yes our their his her my me us about over under "
    "out up down off above below again further once here there all any both each few "
    "more most other some such only own same so than too very s t just"
).split())


# ---------- Loading & chunking ----------
def load_documents(docs_dir=DOCS_DIR):
    docs = []
    for path in sorted(glob.glob(os.path.join(docs_dir, "*.md"))):
        with open(path, "r", encoding="utf-8") as f:
            docs.append({"source": os.path.basename(path), "text": f.read()})
    return docs


def chunk_documents(docs, max_chars=700):
    """Split each doc into paragraph-ish chunks no larger than max_chars."""
    chunks = []
    for d in docs:
        buf = ""
        for part in re.split(r"\n\s*\n", d["text"]):
            part = part.strip()
            if not part:
                continue
            if len(buf) + len(part) + 1 <= max_chars:
                buf = (buf + "\n" + part).strip()
            else:
                if buf:
                    chunks.append({"source": d["source"], "text": buf})
                buf = part
        if buf:
            chunks.append({"source": d["source"], "text": buf})
    for i, c in enumerate(chunks):
        c["id"] = i
    return chunks


# ---------- TF-IDF retrieval (pure standard library) ----------
def tokenize(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower())
            if w not in STOPWORDS and len(w) > 1]


def build_index(chunks):
    tokens_per_chunk = [tokenize(c["text"]) for c in chunks]
    df = Counter()
    for toks in tokens_per_chunk:
        for term in set(toks):
            df[term] += 1
    n = max(len(chunks), 1)
    idf = {term: math.log((n + 1) / (df_t + 1)) + 1 for term, df_t in df.items()}
    vectors = []
    for toks in tokens_per_chunk:
        if not toks:
            vectors.append({})
            continue
        tf = Counter(toks)
        vectors.append({t: (tf[t] / len(toks)) * idf.get(t, 0.0) for t in tf})
    return {"vectors": vectors, "idf": idf}


def _cosine(a, b):
    if not a or not b:
        return 0.0
    num = sum(a[t] * b[t] for t in set(a) & set(b))
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if na and nb else 0.0


def _query_vector(query, idf):
    toks = tokenize(query)
    if not toks:
        return {}
    tf = Counter(toks)
    return {t: (tf[t] / len(toks)) * idf.get(t, 0.0) for t in tf}


def retrieve(query, chunks, index, k=3):
    qv = _query_vector(query, index["idf"])
    scored = [(_cosine(qv, index["vectors"][i]), c) for i, c in enumerate(chunks)]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [(s, c) for s, c in scored[:k] if s > 0]


# ---------- Generation ----------
def build_prompt(query, retrieved):
    context = "\n\n".join(
        f"[{i + 1}] (source: {c['source']})\n{c['text']}"
        for i, (s, c) in enumerate(retrieved)
    )
    return (
        "You are an IT knowledge-base assistant. Answer the user's question using ONLY "
        "the context below. Cite the sources you use inline like [1], [2]. If the answer "
        "is not in the context, say you don't have that information in the knowledge base.\n\n"
        f"CONTEXT:\n{context}\n\nQUESTION: {query}\n\nANSWER:"
    )


def generate_anthropic(query, retrieved):
    import anthropic
    client = anthropic.Anthropic()
    model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest")
    msg = client.messages.create(
        model=model, max_tokens=500,
        messages=[{"role": "user", "content": build_prompt(query, retrieved)}],
    )
    return msg.content[0].text.strip()


def generate_openai(query, retrieved):
    from openai import OpenAI
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    resp = client.chat.completions.create(
        model=model, temperature=0,
        messages=[{"role": "user", "content": build_prompt(query, retrieved)}],
    )
    return resp.choices[0].message.content.strip()


def generate_mock(query, retrieved):
    """Extractive answer: no LLM. Returns the most relevant passage(s) + sources."""
    if not retrieved:
        return "I couldn't find anything relevant in the knowledge base."
    top_text = retrieved[0][1]["text"].strip()
    sources = ", ".join(sorted({c["source"] for s, c in retrieved}))
    return (
        "Based on the knowledge base, the most relevant guidance is:\n\n"
        f"{top_text}\n\n(Sources: {sources})\n"
        "[mock mode: passage retrieved without an LLM. Set LLM_PROVIDER=anthropic or openai "
        "for a synthesized answer.]"
    )


def respond(query, chunks, index, provider=None, k=3):
    retrieved = retrieve(query, chunks, index, k)
    provider = (provider or os.getenv("LLM_PROVIDER", "mock")).lower()
    try:
        if provider == "anthropic":
            answer = generate_anthropic(query, retrieved)
        elif provider == "openai":
            answer = generate_openai(query, retrieved)
        else:
            answer = generate_mock(query, retrieved)
    except Exception as exc:
        sys.stderr.write(f"[warn] {provider} call failed ({exc}); using mock answer.\n")
        answer = generate_mock(query, retrieved)
    return {
        "answer": answer,
        "sources": [{"source": c["source"], "score": round(s, 3)} for s, c in retrieved],
    }


def answer_query(query, k=3, provider=None, docs_dir=DOCS_DIR):
    chunks = chunk_documents(load_documents(docs_dir))
    if not chunks:
        return {"answer": f"No documents found in '{docs_dir}'.", "sources": []}
    index = build_index(chunks)
    return respond(query, chunks, index, provider, k)


def main():
    parser = argparse.ArgumentParser(description="IT Knowledge Base Assistant (RAG)")
    parser.add_argument("query", help="Question to ask the knowledge base")
    parser.add_argument("--provider", help="anthropic | openai | mock")
    parser.add_argument("--k", type=int, default=3, help="Number of passages to retrieve")
    parser.add_argument("--pretty", action="store_true", help="Print full JSON result")
    args = parser.parse_args()

    result = answer_query(args.query, k=args.k, provider=args.provider)
    if args.pretty:
        print(json.dumps(result, indent=2))
        return
    print("=" * 66)
    print("Q:", args.query)
    print("-" * 66)
    print(result["answer"])
    print("-" * 66)
    print("Sources:", ", ".join(f"{s['source']} ({s['score']})" for s in result["sources"]) or "none")
    print("=" * 66)


if __name__ == "__main__":
    main()
