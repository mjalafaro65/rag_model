"""
Simple rag pipeline that answers questions about company policy documents using chromadb for vector storage 
and retrieval , and gemini api for response generation.
"""


import os
from pathlib import Path
from typing import Final
import time


from dotenv import load_dotenv
load_dotenv()


from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

from google import genai
from google.genai import types




#  DOCUMENT LOADING AND CHUNKING
#------------------------------------------------------------------------------- 


ROOT_DIR: Final = "rag_corpus"
N_RESULTS: Final =4

def extract_text():
    """
    Extract text from .md files
    
    """
    
    docs=[]
    # print(ROOT_DIR)
    
    #get all .md files from ROOT_DIR
    for path in Path(ROOT_DIR).glob("**/*.md"):
        #for each .md file
        docs.append({
            "id": str(path.relative_to(ROOT_DIR)),
            "category": path.parent.name,
            "filename": path.name,
            "text":path.read_text(),
        }
            
        )
    return docs


def load_chunk_documents():
    """
    Gets extracted text from files and chunk them
    
    
    steps
        1.get text
        2.define text splitter
        3.iterate through docs and chunk it using text splitter
    
    """
    
    
    
    #extracted text from files
    docs=extract_text()
    
    
    #define splitter
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n## ","\n\n", "\n" ," ",""]
    )
    
    
    #chunk text
    all_chunks= []
    
    for doc in docs: 
        
        chunks=text_splitter.split_text(doc["text"])
        
        for i, chunk in enumerate(chunks):
            
            all_chunks.append({
                "id": f"{doc["id"]}_chunk_{i}",
                "filename": doc["filename"],
                "content": chunk,
                "category": doc["category"],
                "source_doc_id": doc["id"],
                
            })
    
    # print(all_chunks)
    return all_chunks


#  VECTOR DATABASE SETUP
#-------------------------------------------------------------------------------

#define embedding function
    

def setup_vector_database(chunks):
    """
    Set up chromadb database and store chunks
    
    1.create chroma client
    3.create collection
    4.prepare chunks for storage
    5.add chunks to collection
    
    """
    
    #create client
    chroma_client = chromadb.PersistentClient()
    
    
    
   
    #create collection to store embeddings
    try:
        collection = chroma_client.create_collection(
            name="corp_docs", #collection name
            metadata={"hnsw:space":"cosine"}, #similarity metric used
        )
        
    except Exception:
        collection=chroma_client.get_collection("corp_docs")
        
        
       
    #prepare for storage
    ids=[chunk["id"] for chunk in chunks]
    documents=[ chunk["content"] for chunk in chunks]
    metadatas=[ {"filename": chunk['filename'], "category": chunk['category'],"source": chunk['source_doc_id']} for chunk in chunks]
    
    
    #add to collection
    if collection.count() ==0:    
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
    
    else:
        print(f"Collection in database has {collection.count()} chunks")
        
        
    return collection
    
    
#  query processing
#-------------------------------------------------------------------------------    
def process_query(query):
    #embedding model
    
    
    #preprocess query, simple is better
    return query.lower().strip()
    
    
     

   
    

#  Vector search
#-------------------------------------------------------------------------------
        
def  search_database(collection, query, results=N_RESULTS ):
    """
        Run search, return results as a list, and make it readable
    """
    
    
    #vector search
    results=collection.query(
        query_texts=[query],
        n_results=results   #number of results returned
        
    )
    
    ####TO PRINT CHROMADB RESULTS:#######################
    # print("Results from database:----------------------------------------------------------------- \n")
    # print(results)
    ####TO PRINT CHROMADB RESULTS:#######################


    #process results
     
    processed_results=[]
    for (chunk_id,content,metadatas,distances) in zip(results["ids"][0],results["documents"][0], results["metadatas"][0], results["distances"][0]):
        
        processed_results.append({
            "ids": chunk_id,
            "content" : content ,
            "metadatas": metadatas,
            "distances" : distances
        })
    
    ####TO PRINT CHROMADB PROCESSED RESULTS: ##############################
    #print("\nResults after formatting:-----------------------------------------------------------------\n")
    #print(processed_results)
    ####TO PRINT CHROMADB RESULTS:#######################

     
    return processed_results
    
    
    
    
#  Context augmentation
#-------------------------------------------------------------------------------
       
def augmented_prompt_with_context(query, search_results):
    """
     Build augmented prompt with context retrieved from database
     
      1.Retrieve context from search results 
      2.prompt construction
    """
    
    #take needed information form search result 
    context_sections=[]
    for i, result in enumerate(search_results,1):
        context_sections.append(f"Number{i}: {result["metadatas"]["filename"]}\n{result["content"]}")
    
    #forms string separated by two lines from list 
    context="\n\n".join(context_sections)
    #make prompt
    augmented_prompt=f"""
        Use the following company's policy to answer the user's question:
        
        
        POLICIES:
        {context}
        
        QUESTION:
        {query}
        
        Please provide a clear and accurate answer based on the policies above.
        If relevant information is not available in the provided policies above say so.
        Include relevant policy details and any limitations or requirements.
        
    
        
    """
    
    return augmented_prompt
  

def generate_response(augmented_prompt):
    """
        Send augmented prompt to gemini and return response
        
        
    
    """
    
    client=genai.Client()  
    
    retries=2
    for attempt in range(retries):
        try:
            response=client.models.generate_content(
                model="gemini-3.6-flash",
                contents=augmented_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2, #Test: low temperatures, response sticks strictly to provided content
                    system_instruction=(
                        "You are a strict company policy assistant. Answer the user's question using only the provided context. If the answer cannot be found in context, state clearly that you do not have enough information "
                    )
                )  
            )
            return response.text
            
            
        except Exception as e:
            if "503" in str(e) and attempt < retries-1:
                time.sleep(2)
                continue
            print(f"Error generating response {e}")
            return None
        
    
    
    
    
    

#  Rag Pipeline 
#-------------------------------------------------------------------------------

def main():
    
    chunks=load_chunk_documents()
    
    collection=setup_vector_database(chunks)
    
    queries=["What happens during first week for new hires",
             "What are the rules for using company systems and personal devices?",
             "What happens if an employee violates the acceptable use policy?",
              "What does the policy say about VPN and public Wi-Fi for remote workers?"
             ]
    for i,query in enumerate(queries,1):
       
        # print(collection)
        processed_query=process_query(query)

        search_results=search_database(collection,processed_query)
            
        augmented_prompt=augmented_prompt_with_context(query,search_results)
            
        response=generate_response(augmented_prompt)


        print(f"\n-----RESULTS FROM QUERY #{i}------------------------------------------------------------")

        print(response)
        
        print(f"-----END OF RESULTS FROM QUERY #{i}------------------------------------------------------------\n\n\n")
            
    
    
            
if __name__ == "__main__":
    main()         
            


  