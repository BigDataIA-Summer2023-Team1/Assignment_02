## Live application Links :octopus:

- Please use this application responsibly, as we have limited free credits remaining.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)]()

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)]()

[![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-007A88?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)]()

[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1JDqgTg8wtQyI5s-jvMLUf8tCtqtrd3sxw8xzP2gR32o)

[![Notes](https://img.shields.io/badge/Notes:_Document_Deduplication-violet?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1wZHwpf0NhYRnSY4tommwI5MUKERujjwsK_1NMKvp8wo)

## Problem Statement :memo:
Intelligence Co, a financial research firm, wants to explore the potential of large language models by building a contextual search application for their investment analysts. The application should allow analysts to search through earnings call transcripts using vector similarity search, traditional filtering, and hybrid search techniques. The company has approached our team to develop this application, which will involve data exploration, search functionality, and deployment using various tools such as Airflow, Redis, Streamlit, FastAPI, and Docker. The primary goal is to create an efficient and user-friendly platform that enables analysts to filter transcripts based on company and year, ask specific questions, and retrieve relevant responses. The application should also incorporate a workflow to process the dataset, compute embeddings using SBERT and OpenAI models, and implement a Q/A system using VSS with RAG. Security measures, such as authentication with API keys, should be implemented to safeguard sensitive information. The final deliverables include a hosted Streamlit application, a documented codebase on GitHub, and comprehensive test cases and results analysis.

## Project Goals :dart:
Task -1:

Task -2:

Task -3:

Task -4:

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

## Project Structure

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

## Problems Resolved

## Team Information and Contribution 
Name | Contributions 
--- | --- |
Sanjana Karra | 
Nikhil Reddy Polepally | 
Shiva Sai Charan Ruthala | 
