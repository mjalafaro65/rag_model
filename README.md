A Retrieval-Augmented Generation (RAG) pipeline that answers questions about company policy documents. It retrieves the most relevant policy excerpts from a vector database and uses Google's Gemini API to generate answers — explicitly refusing to answer when the information isn't in the provided documents.

How It Works
 1.Document Loading — Markdown policy files are read from rag_corpus/ (organized by category: onboarding, HR policies, IT/security policies, engineering guidelines, legal/compliance).
 2. Chunking — Documents are split into overlapping chunks using RecursiveCharacterTextSplitter.
 3.Embedding & Storage — Chunks are embedded and stored in a persistent ChromaDB collection, so documents are only embedded once and reused across runs.
 4.Retrieval — A user's query is embedded and matched against the collection using cosine similarity to pull the most relevant chunks.
 5.Augmentation — Retrieved chunks are assembled into a prompt alongside the user's question.
 6.Generation — The augmented prompt is sent to Gemini (gemini-3.6-flash) with a low temperature and a strict system instruction to answer only from the provided context, and to say so explicitly when the answer isn't covered.

