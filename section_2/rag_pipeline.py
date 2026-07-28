import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

DB_HF_PATH = "faiss_index"

def build_rag_pipeline():
    # 1. Load documents
    docs_dir = os.path.join(os.path.dirname(__file__), "sample_docs")
    loader = DirectoryLoader(docs_dir, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()

    # 2. Chunk documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Loaded {len(documents)} documents, split into {len(chunks)} chunks.")

    # 3. Clean up existing FAISS Database
    if os.path.exists(DB_HF_PATH):
        print("FAISS vectorstore already exists. Deleting it to rebuild.")
        shutil.rmtree(DB_HF_PATH)

    # 4. Embed and store in FAISS (Using Free Local HuggingFace Embeddings)
    hf_embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=hf_embeddings
    )

    # Save FAISS index locally
    vectorstore.save_local(DB_HF_PATH)
    
    total_vectors = vectorstore.index.ntotal
    dimensions = vectorstore.index.d
    print(f"Successfully built FAISS vector store with {total_vectors} vectors and {dimensions:,} dimensions.")

    return vectorstore

def sampling_vector(vectorstore: FAISS, vector_index: int) -> None:
    # Get document ID linked to vector index
    doc_id = vectorstore.index_to_docstore_id[vector_index]
    
    # Search in docstore using the ID
    document = vectorstore.docstore.search(doc_id)
    print(f"--- Sampling Vector at Index {vector_index} ---")
    print(f"Metadata & Document Context:\n{document}\n")
    
    # Retrieve the actual vector values (embedding)
    sample_vector = vectorstore.index.reconstruct(vector_index)
    print(f"This vector has {len(sample_vector)} dimensions. First 5 dims:\n{sample_vector[:5]}\n")

def run_rag_chain(vectorstore: FAISS):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # 5. Build LangChain with fallback guardrail using HuggingFace Endpoint (Free API)
    # Requires HF_TOKEN environment variable
    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-7B-Instruct",
        max_new_tokens=256,
        temperature=0.1
    )
    chat_llm = ChatHuggingFace(llm=llm)
    
    # Custom prompt explicitly instructing not to hallucinate
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If the answer is not contained in the context, explicitly state: "
        "'I cannot answer this question based on the provided context.' "
        "Do not make up an answer.\n\n"
        "Context:\n{context}"
    )

    prompt = PromptTemplate.from_template(system_prompt)
    question_answer_chain = create_stuff_documents_chain(chat_llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # 3 Example questions
    questions = [
        # Question 1: Extractable from doc1.md
        "How long do candidates have to complete the technical test?",
        # Question 2: Extractable from doc2.md
        "What vector databases are mentioned for storing embeddings?",
        # Question 3: Not in context (testing fallback)
        "Who won the world cup in 2022?"
    ]

    for i, q in enumerate(questions, 1):
        print(f"\n--- Example {i} ---")
        print(f"Q: {q}")
        
        response = rag_chain.invoke({"input": q})
        answer = response["answer"]
        source_docs = response.get("context", [])
        
        print(f"A: {answer}")
        
        # Determine citations
        if "I cannot answer this question" not in answer:
            print("Citations:")
            for j, doc in enumerate(source_docs, 1):
                source_file = os.path.basename(doc.metadata.get("source", "Unknown"))
                print(f"  [{j}] Source: {source_file}")
                snippet = doc.page_content.replace("\n", " ")[:60]
                print(f"      Content: \"{snippet}...\"")
        else:
            print("Citations: None (Fallback triggered)")

def main():
    if not os.environ.get("HF_TOKEN"):
        print("Warning: HF_TOKEN not found. Please set it in your environment to run the HuggingFace LLM pipeline.")
        # We will still build the FAISS index to prove that works without an API key
        
    print("Building RAG pipeline...")
    vectorstore = build_rag_pipeline()
    
    # Sample the very first vector created
    if vectorstore.index.ntotal > 0:
        sampling_vector(vectorstore, 0)

    if os.environ.get("HF_TOKEN"):
        run_rag_chain(vectorstore)

if __name__ == "__main__":
    main()
