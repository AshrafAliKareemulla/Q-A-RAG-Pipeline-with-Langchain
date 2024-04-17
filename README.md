# RAG-Based Q&A Chatbot Pipeline Utilizing Langchain :rocket:

## About RAG Application using Langchain Framework :zap:
<style>
    body {
        font-family: 'Times New Roman', Times, serif;
    }
</style>

Retrieval Augmented Generation is an LLM-based question answering system. This acts as a chatbot when used with Chainlit framework.
Let's look at the RAG pipeline architecture.

1. Load Source Data
   - Load the data from multiple sources like text, pdfs, web based loaders, etc.
   - Transform the data i.e divide it into chunks.
   - Create Embeddings either using OpenAI/Ollama embeddings or any other.
2. Query Database :mag:
3. Retrieve most similar answer to the query.



<div align = 'center'>

<img src="Output_Images/Pipeline.png" alt="RAG PIPELINE" width="75%" height="300">

</div> 
<br>





## Detailed overview of the RAG Pipelining

1. Many data sources like pdfs, markdown files, text files, excel sheets, web content, image, etc are present and we need some Data Ingestion tools to load these information.

2. The first step in creation of the application is using data ingestion tools like text based loaders, pdf based loaders, web based loaders, etc. We use PyPDFLoader to load all the given pdfs.

3. Next, we transform the data i.e divide the data into smaller chunks so that we don't exceed the context size of the LLM models.

4. Use embeddings and convert the data chunks into vectors.

5. All these vectors are further stored in a vector store database like Typesense, Chroma, FAISS, etc.

6. Now we combine prompts along with chains and retrieval & get a response.

7. Vector store has some vectors and if we want any data from that, we can do similarity search but it is not effective. So, Retriever are used as an interface so that it has access to the vector store.

8. So, now we create a chain & retriever. Using these, we create a retriever chain where this chain takes in a user query, which is then passed to the retriever to fetch relevant documents. Those documents are then passed to an LLM to generate a response. 





<div align = 'center'>

<img src="Output_Images/Retrieval_Chain.png" alt="Retrieval Chain" width="75%" height="300">

</div>

<br>






## Steps to run the RAG Application

- Clone the repository
```bash
git clone https://github.com/KareemullaAshrafAli/Q-A-RAG-Pipeline-with-Langchain.git
```


- Install all the required libraries given in the requirements.txt file
```bash
pip install -r requirements.txt
```


- To start running the Typesense cloud server, visit [Typesense Cloud Cluster](https://cloud.typesense.org/clusters) to create a cluster and you will get a page as shown below.



<div align = 'center'>

<img src="Output_Images/Typesense_Cluster.png" alt="Typesense Cloud Cluster" width="75%" height="300">

</div>


- Now, click on generate API Keys, a text file :page_facing_up: with typesense admin key will be downloaded. Node name i.e host name is in the above picture (Ex : xxx.a1.typesense.net).


- Now, Create a .env file :page_with_curl: and add your OpenAI API key, Typesense Host and Typesense Admin API Key in it as follows
```bash
OPENAI_API_KEY = "enter_your_openai_api_key"
TYPESENSE_HOST = "enter_your_cloud_host_name"
TYPESENSE_API_KEY = "enter_your_admin_api_key"
```

- Run the below command to host chainlit user interface.
```bash
chainlit run app.py -w
```    

- set `vector_store = "chroma"` or `vector_store = "faiss"` in 31st line of `app.py` file to use them as vector stores instead of typesense.



## Response of OpenAI's ChatGPT 3.5 Turbo Model :maple_leaf:



<div align = 'center'>

<img src="Output_Images/result_1.png" alt="Result - 1" width="75%" height="350"> <br>
<img src="Output_Images/result_2.png" alt="Result - 2" width="75%" height="350"> <br>
<img src="Output_Images/result_3.png" alt="Result - 3" width="75%" height="350">

</div>

<br>