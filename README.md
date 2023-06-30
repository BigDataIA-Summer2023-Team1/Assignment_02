## Live application Links :octopus:

- Please use this application responsibly, as we have limited free credits remaining.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](http://34.139.252.216:30006/)

[![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-007A88?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](http://34.139.252.216:8080/)

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)]()

[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1JDqgTg8wtQyI5s-jvMLUf8tCtqtrd3sxw8xzP2gR32o)

[![Notes](https://img.shields.io/badge/Notes:_Document_Deduplication-violet?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1wZHwpf0NhYRnSY4tommwI5MUKERujjwsK_1NMKvp8wo)

## Problem Statement :memo:
Intelligence Co, a financial research firm, wants to explore the potential of large language models by building a contextual search application for their investment analysts. The application should allow analysts to search through earnings call transcripts using vector similarity search, traditional filtering, and hybrid search techniques. The company has approached our team to develop this application, which will involve data exploration, search functionality, and deployment using various tools such as Airflow, Redis, Streamlit, FastAPI, and Docker. The primary goal is to create an efficient and user-friendly platform that enables analysts to filter transcripts based on company and year, ask specific questions, and retrieve relevant responses. The application should also incorporate a workflow to process the dataset, compute embeddings using SBERT and OpenAI models, and implement a Q/A system using VSS with RAG. Security measures, such as authentication with API keys, should be implemented to safeguard sensitive information. The final deliverables include a hosted Streamlit application, a documented codebase on GitHub, and comprehensive test cases and results analysis.

## Project Goals :dart:
Task -1:
Data Ingestion: Copy all data from the github and store in Google Cloud storage and Store the metadata (Name, date, quarter, month, ticker symbol, Google cloud
storage location of the file) in Google cloud SQL (Postgres SQL)

Task -2:
Build a streamlit application that would:
1. Expose the metadata stored in the Google cloud storage as dropdowns for
   selection
2. Once a user selects a file, get the file and compute the summaries using OpenAI.
3. If the user wants to search or ask questions regarding the chosen document:
   Obtain the full transcript, Chunk and tokenize it and compute embeddings that are stored in
   pinecone,  implement a Q/A interface on Streamlit 

Task -3:
Redo the Task-2 using langchain and pinecone and compare it with Task-2


Task -4:
Discuss what approach you would use and why you think the components are the best for the use case which include a technical design specification on how to
accomplish your design

## Technologies Used :computer:
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Apache Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![GitHub Actions](https://img.shields.io/badge/Github%20Actions-282a2e?style=for-the-badge&logo=githubactions&logoColor=367cfe)](https://github.com/features/actions)
![gcp provider](https://img.shields.io/badge/GCP-orange?style=for-the-badge&logo=google-cloud&color=orange)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![Codelabs](https://img.shields.io/badge/Codelabs-violet?style=for-the-badge)

## Data Source :flashlight:
1. Companies earnings call dataset: https://github.com/Earnings-Call-Dataset/MAEC-A-Multimodal-Aligned-Earnings-Conference-Call-Dataset-for-Financial-Risk-Prediction/tree/master/MAEC_Dataset
2. Ticker data: https://github.com/plotly/dash-stock-tickers-demo-app/blob/master/tickers.csv

## Requirements
```
requests
SQLAlchemy
python-dotenv
cloud-sql-python-connector
cloud-sql-python-connector[pg8000]
langchain
openai==0.27.7
tiktoken==0.4.0
google-cloud-storage==2.9.0
protobuf==3.19.3
streamlit==1.22.0
pinecone-client[grpc]==2.2.1
```

## Project Structure
```
📦 Assignment_02
├─ .gitignore
├─ Makefile
├─ README.md
├─ airflows
│  ├─ .gitignore
│  ├─ Dockerfile
│  ├─ dags
│  │  ├─ extract_earnings_call_data.py
│  │  ├─ gcs_service.py
│  │  └─ sql.py
│  └─ requirements.txt
├─ api
│  ├─ .gitignore
│  ├─ Dockerfile
│  ├─ main.py
│  ├─ requirements.txt
│  └─ utils.py
├─ architecture
│  └─ requirements.txt
├─ docker-compose-local.yml
├─ frontend
│  ├─ .gitignore
│  ├─ Dockerfile
│  ├─ main.py
│  ├─ pages
│  │  ├─ 1_screen_1.py
│  │  ├─ 2_screen_2.py
│  │  └─ 3_screen_3.py
│  └─ requirements.txt
└─ terraform
   ├─ .gitignore
   ├─ Makefile
   ├─ install.sh
   ├─ main.tf
   ├─ output.tf
   └─ variables.tf
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)

## How to run Application locally

To run the application locally, follow these steps:
1. Clone the repository to get all the source code on your machine.

2. Install docker desktop on your system

3. Create a .env file in the root directory with the following variables:
    ``` 
        # Github Variables
        TICKER_DATA_FILE=https://raw.githubusercontent.com/plotly/dash-stock-tickers-demo-app/master/tickers.csv 
        STOCK_TICKER_DATA_FILE=https://raw.githubusercontent.com/plotly/dash-stock-tickers-demo-app/master/stock-ticker.csv
        
        REPO_OWNER='Earnings-Call-Dataset'
        REPO_NAME='MAEC-A-Multimodal-Aligned-Earnings-Conference-Call-Dataset-for-Financial-Risk-Prediction' 
    ```

4. Once you have set up your environment variables, Start the application by executing
    ``` 
        Make build-up
    ```

5. Once all the docker containers spin up, Access the application at following links
    ``` 
         1. Stremlit UI: http://localhost:30006/
         2. FAST API   : http://localhost:30005/docs
         
         # Airflow Credentials - username: airflow; password: airflow
         3. Airflow    : http://localhost:8080/  
    ```

6. To delete all active docker containers execute
    ``` 
         Make down
    ``` 


## References
1. OpenAI notes Summary - https://platform.openai.com/examples/default-notes-summary
2. LangChain Retrieval - https://alphasec.io/summarize-documents-with-langchain-and-pinecone/
3. LangChain Retrieval - https://docs.pinecone.io/docs/langchain-retrieval-agent
4. CloudSQL - https://cloud.google.com/sql/docs/postgres
5. Pinecone - https://docs.pinecone.io/docs/overview
6. Architecture Diagrams - https://github.com/mingrammer/diagrams

## Learning Outcomes
1. How to leverage langchain package to build chatbots based on our data.
2. 

## Team Information and Contribution 
Name | Contributions 
--- | --- |
Sanjana Karra | Implemented generative question & answering using langchain, Documentation
Nikhil Reddy Polepally | Designed and build Streamlit UI & storing, indexing vector embeddings on pinecone DB, Drawn a architecute diagram.
Shiva Sai Charan Ruthala | Implemented airflow pipelines to to ingest data from github to GCS and Google Cloud SQL & Deployed application on GCP
