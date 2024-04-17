from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS,Typesense
from langchain_openai import OpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
import chainlit as cl
from itertools import chain
import os
from dotenv import load_dotenv






# Load the environment
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")



# Replace with "chroma" or "faiss" for other vector stores
vector_store = "typesense"  








def load_pdfs():
    pdf0 = PyPDFLoader('TextBook_PDF/fepw1ps.pdf').load()
    pdf1 = PyPDFLoader('TextBook_PDF/fepw101.pdf').load()
    pdf2 = PyPDFLoader('TextBook_PDF/fepw102.pdf').load()
    pdf3 = PyPDFLoader('TextBook_PDF/fepw103.pdf').load()
    pdf4 = PyPDFLoader('TextBook_PDF/fepw104.pdf').load()
    pdf5 = PyPDFLoader('TextBook_PDF/fepw105.pdf').load()
    pdf6 = PyPDFLoader('TextBook_PDF/fepw106.pdf').load()
    pdf7 = PyPDFLoader('TextBook_PDF/fepw107.pdf').load()

    return pdf0, pdf1, pdf2, pdf3, pdf4, pdf5, pdf6, pdf7











def text_splitter(pdf0, pdf1, pdf2, pdf3, pdf4, pdf5, pdf6, pdf7):
    text_split = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    pdf_docs0 = text_split.split_documents(pdf0)
    pdf_docs1 = text_split.split_documents(pdf1)
    pdf_docs2 = text_split.split_documents(pdf2)
    pdf_docs3 = text_split.split_documents(pdf3)
    pdf_docs4 = text_split.split_documents(pdf4)
    pdf_docs5 = text_split.split_documents(pdf5)
    pdf_docs6 = text_split.split_documents(pdf6)
    pdf_docs7 = text_split.split_documents(pdf7)
    return pdf_docs0, pdf_docs1, pdf_docs2, pdf_docs3, pdf_docs4, pdf_docs5, pdf_docs6, pdf_docs7












@cl.on_message
async def main(message: cl.Message):
    

    # Load all the pdfs
    pdf0, pdf1, pdf2, pdf3, pdf4, pdf5, pdf6, pdf7 = load_pdfs()


    # Transform i.e split all the PDFs into chunks for storing in vector db
    doc0, doc1, doc2, doc3, doc4, doc5, doc6, doc7 = text_splitter(pdf0, pdf1, pdf2, pdf3, pdf4, pdf5, pdf6, pdf7)


    # Flatten all the pdfs
    flattened_docs = list(chain.from_iterable([doc0, doc1, doc2, doc3, doc4, doc5, doc6, doc7]))


    # Create OpenAI model i.e chatgpt-3.5-turbo-instruct and chat prompt template
    openai_model = OpenAI(model="gpt-3.5-turbo-instruct")
    
    prompt = ChatPromptTemplate.from_template("""
    Answer the following Question based only on the provided context.
    Think step by step before providing a detailed answer.
    <context>
    {context}                                              
    </context>                                            
    Question : {input}""")




    # Create a chain
    doc_chain = create_stuff_documents_chain(openai_model, prompt)



    # Create vector stores & corresponding retrievers

    if (vector_store == "typesense"):
        typesense_db = Typesense.from_documents(
        flattened_docs,
        OpenAIEmbeddings(),
        typesense_client_params = {
        "host" : "czuxlts9ma6pewkdp-1.a1.typesense.net",
        "port" : "443",
        "protocol" : "https",
        "typesense_api_key" : "nezaUQR27h4ClkDLgC32nS0wKFaGmBCb",
        "typesense_collection_name" : "lang-chain"
        },)

        retriever = typesense_db.as_retriever()


    elif (vector_store == "chroma"):
        chroma_db = Chroma.from_documents(flattened_docs, OpenAIEmbeddings())
        retriever = chroma_db.as_retriever()


    elif (vector_store == "faiss"):
        faiss_db = FAISS.from_documents(flattened_docs, OpenAIEmbeddings())
        retriever = faiss_db.as_retriever()

    
    # Create a retriever chain
    retriever_chain = create_retrieval_chain(retriever, doc_chain)

    # Invoke the chain to get response
    response = retriever_chain.invoke({"input" : message.content})


    
    
    # Send a response back to the user
    await cl.Message(
        content = response['answer'],
    ).send()