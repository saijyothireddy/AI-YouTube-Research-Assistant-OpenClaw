from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(text_chunks):
    embeddings = model.encode(text_chunks)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index, text_chunks

def retrieve(query, index, chunks):
    q = model.encode([query])
    _, I = index.search(np.array(q), 3)
    return " ".join([chunks[i] for i in I[0]])
