from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from .models import Message

model = SentenceTransformer("all-MiniLM-L6-v2")


def get_rag_context(user_message, conversation_id):
    memory_msgs = Message.objects.filter(
        conversation_id=conversation_id
    ).order_by("-id")[:5]

    memory_docs = [m.content for m in memory_msgs]

    #  2. GLOBAL RAG (last 50 messages)
    all_msgs = Message.objects.all().order_by("-id")[:50]

    global_docs = [m.content for m in all_msgs]

    #  3. Combine
    documents = memory_docs + global_docs

    #  If no data
    if not documents:
        return ""

    #  4. Convert to embeddings
    doc_embeddings = model.encode(documents)

    index = faiss.IndexFlatL2(doc_embeddings.shape[1])
    index.add(np.array(doc_embeddings))

    #  5. Search
    query_embedding = model.encode([user_message])
    D, I = index.search(np.array(query_embedding), k=3)

    results = [documents[i] for i in I[0]]

    return "\n".join(results)
