import os
import time
import requests

import streamlit as st

from uuid import uuid4
from dotenv import load_dotenv

from sqlalchemy import text, create_engine
from google.cloud.sql.connector import Connector

import openai
import tiktoken
import pinecone
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader


load_dotenv("../.env")


def connect_to_sql():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./storage-key.json"

    return Connector().connect(
        instance_connection_string=os.environ['INSTANCE_CONNECTION_NAME'],
        driver=os.environ["DB_DRIVER"],
        user=os.environ["DB_USER"],
        password=os.environ['DB_PASS'],
        db=os.environ["DB_NAME"]
    )


def get_sql_client(conn):
    return create_engine("postgresql+pg8000://", creator=conn).connect()


def fetch_companies_from_db():
    conn = get_sql_client(connect_to_sql)

    q = text('SELECT DISTINCT company from earnings_transcript_meta_data')

    # Execute the query
    result = conn.execute(q)

    # Fetch all the rows returned by the query
    rows = result.fetchall()

    companies_list = []
    # Process the rows
    for row in rows:
        companies_list.append(row.company)

    conn.close()

    return companies_list


def fetch_years_from_db():
    conn = get_sql_client(connect_to_sql)

    q = text("SELECT DISTINCT DATE_PART('year', financial_year) AS year FROM earnings_transcript_meta_data")

    # Execute the query
    result = conn.execute(q)

    # Fetch all the rows returned by the query
    rows = result.fetchall()

    years_list = []
    # Process the rows
    for row in rows:
        years_list.append(int(row.year))

    conn.close()

    return years_list


@st.cache_data
def fetch_company_metadata(company, year):
    conn = get_sql_client(connect_to_sql)

    formatted_query = "SELECT company, ticker, financial_year, quarter, uri FROM earnings_transcript_meta_data where company = '{}' and DATE_PART('year', financial_year) = '{}'".format(
        company, year)
    print(formatted_query)
    q = text(formatted_query)

    # Execute the query
    result = conn.execute(q)

    # Fetch all the rows returned by the query
    rows = result.fetchall()

    metadata = []
    # Process the rows
    for row in rows:
        metadata.append({"company": row.company, "ticker": row.ticker, "quarter": row.quarter, "uri": row.uri,
                         "timestamp": row.financial_year})

    conn.close()

    return metadata


def get_earnings_call_data(url):
    response = requests.get(url)

    # Check the status code to ensure the request was successful
    if response.status_code == 200:
        # Print the response content
        return response.text
    else:
        print("Error:", response.status_code)
        return ""


@st.cache_data
def text_summarization(api_key, prompt):
    openai.api_key = api_key

    return openai.Completion.create(
        model="text-davinci-003",
        prompt="Brief the companies financial earnings transcript \n\n {}".format(prompt),
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )


tiktoken.encoding_for_model('gpt-3.5-turbo')


def tiktoken_len(query):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(
        query,
        disallowed_special=()
    )
    return len(tokens)


def text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=["\n\n", "\n", " ", ""]
    )


def openai_embeddings(openai_key):
    return OpenAIEmbeddings(
        model='text-embedding-ada-002',
        openai_api_key=openai_key
    )


@st.cache_data
def index_vectors(openai_key, pinecone_key, pinecone_environment, index_name, query, company_metadata):
    chunks = text_splitter().split_text(query)

    record_metadata = [{
        "chunk": j, "text": chunk_text, **company_metadata
    } for j, chunk_text in enumerate(chunks)]

    pinecone.init(
        api_key=pinecone_key,
        environment=pinecone_environment
    )

    if index_name not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(
            name=index_name,
            metric='cosine',
            dimension=1536
        )

    if "vector_ids" in st.session_state and len(st.session_state["vector_ids"]) > 0:
        p_index = pinecone.Index(index_name)
        p_index.delete(ids=st.session_state["vector_ids"])

    index = pinecone.GRPCIndex(index_name)
    time.sleep(20)

    if len(chunks) > 0:
        ids = [str(uuid4()) for _ in range(len(chunks))]
        st.session_state["vector_ids"] = ids
        embeds = openai_embeddings(openai_key).embed_documents(chunks)

        index.upsert(vectors=zip(ids, embeds, record_metadata))
        print("Indexing Completed")

def process_query(input_query,PINECONE_API_KEY,PINECONE_ENVIRONMENT,INDEX_NAME,OPENAI_API_KEY):
    text_field = "text"

    pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENVIRONMENT
    )

    # Switch back to the normal index for langchain
    index = pinecone.Index(INDEX_NAME)

    vectorstore = Pinecone(index, openai_embeddings(OPENAI_API_KEY).embed_query, text_field)

    # # Perform similarity search using vectorstore
    # search_results = vectorstore.similarity_search(
    #     input_query,  # Our search query
    #     k=3  # Return 3 most relevant documents
    # )

    # Create the Language Model (LLM) for completion
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )

    # Create a Retrieval QA chain with sources
    qa = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    # Process the query using the QA chain
    result = qa(input_query)

    return result


# Streamlit app
st.subheader('Text Summarization')

st.session_state['vector_ids'] = []

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API key", type="password")
    pinecone_api_key = st.text_input("Pinecone API key", type="password")
    pinecone_env = st.text_input("Pinecone environment")
    pinecone_index = st.text_input("Pinecone index name")

with st.form("login", clear_on_submit=False):
    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        companies_list = fetch_companies_from_db()

        company_name = st.selectbox(
            'Company Name', companies_list)
        st.write('You selected:', company_name)

    with col2:
        years = fetch_years_from_db()

        financial_year = st.selectbox(
            'Financial Year', years)

        st.write('You selected:', financial_year)

    show_data_btn = st.form_submit_button("Show Meta Data")

if show_data_btn:
    data = fetch_company_metadata(company_name, financial_year)
    st.session_state['metadata'] = data

    st.write("Metadata")
    st.json(data)

    st.write("Earnings Call Data")
    source_blob_url = "https://storage.googleapis.com/earnings-call-data-new-bucket/dataset/{}".format(
        data[0]["uri"].split("/")[
            -1])  # TODO: Let user choose the file from UI and fetch that specifc call data from the GCS
    earnings_call_data = get_earnings_call_data(source_blob_url)

    st.session_state['earnings_call_data'] = earnings_call_data

    st.text_area("", value=earnings_call_data, height=300)

    if openai_api_key and pinecone_api_key and pinecone_env and pinecone_index:
        earnings_call_data_summary = text_summarization(openai_api_key, earnings_call_data)


        
        st.write("Earnings Call Data Summary: ")
        st.text_area("", value=earnings_call_data_summary.choices[0].text, height=300)
        

        metadata = {'company': data[0]["company"], 'ticker': data[0]["ticker"],
                    'quarter': data[0]["quarter"], 'source': data[0]["uri"]}

        index_vectors(openai_api_key, pinecone_api_key, pinecone_env, pinecone_index, earnings_call_data, metadata)

    else:
        st.warning(f"Please provide the missing fields.")

    

input_query = st.text_area("Your Query Here: ", "")
search_btn = st.button("Search")
if search_btn:
    qa_with_sources = process_query(input_query,pinecone_api_key,pinecone_env,pinecone_index,openai_api_key)
    st.write("Generative Questioning Answering using Langchain")
    st.json(qa_with_sources)