# uses FAISS (Facebook AI Similarity Search) to build an index for fast approximate nearest-neighbor similarity search on protein vectors
import logging
import faiss
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def build_index(embeddings: np.ndarray):
    # builds a FAISS index from embedding vectors
    # uses cosine similarity (normalize, then inner product)
    norms = np.linalg.norm(embeddings, keepdims=True)
    normalized = embeddings / (norms + 1e-8)
    dim = normalized.shape[1]
    index = faiss.IndexFlatIP(dim)

def search(faiss_index, query_embedding, top_k=5):
    # searches the index for the top k nearest results for the query
    # returns (distances, indices) where distances is cosine similarity
    # normalize the embeddings
    norms = np.linalg.norm(query_embedding, keepdims=True)
    normalized_query = (query_embedding/(norms + 1e-8)).astype("float32").reshape(1, -1)

    # cosine similarity search
    distances, indices = index.search(normalized_query, top_k)
    return distances[0], indices[0]

if __name__ == "__main__":
    embeddings = np.load()
    build_index(embeddings)