import os
import datetime
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import timedelta

from airflow.models import DAG
from airflow.models.param import Param
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

from gcs_service import upload_file_to_gcs, write_to_file, delete_file
from sql import connect_to_sql, get_sql_client, insert_to_table, create_table


# load env variables
load_dotenv('../../.env')


def fetch_companies_data():
    ticker_data = pd.read_csv(str(os.getenv("TICKER_DATA_FILE",
                                            'https://raw.githubusercontent.com/plotly/dash-stock-tickers-demo-app/master/tickers.csv'))).set_index('Symbol')['Company']  # .to_dict()

    return ticker_data


def fetch_files_from_repo():
    repo_owner = os.getenv("REPO_OWNER", 'Earnings-Call-Dataset')
    repo_name = os.getenv("REPO_NAME",
                          'MAEC-A-Multimodal-Aligned-Earnings-Conference-Call-Dataset-for-Financial-Risk-Prediction')

    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/MAEC_Dataset'

    # Fetch the contents of the repository
    response = requests.get(base_url)
    response.raise_for_status()
    files = response.json()

    return files


def fetch_earnings_call_data(file_name):
    repo_owner = os.getenv("REPO_OWNER", 'Earnings-Call-Dataset')
    repo_name = os.getenv("REPO_NAME",
                          'MAEC-A-Multimodal-Aligned-Earnings-Conference-Call-Dataset-for-Financial-Risk-Prediction')

    raw_url = f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/master/MAEC_Dataset/{file_name}/text.txt'
    response = requests.get(raw_url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return ""


def batch_generator(data, batch_size, batch_counter=0):
    for i in range(0, len(data), batch_size):
        batch_counter += 1
        yield batch_counter, data[i:i+batch_size]


def upload_files(**context):
    batch_size = context['params']['file_upload_batch_size']

    files = fetch_files_from_repo()
    companies_ticker_mapping = fetch_companies_data()

    no_of_batches = len(files)/batch_size

    for batch_no, batch_files in batch_generator(files, batch_size):
        company_meta_data = []

        for file in batch_files:
            timestamp = file['name'].split("_")[0]
            year = timestamp[0:4]
            month = timestamp[4:6]
            date = timestamp[6:]
            quarter = ""

            if 1 <= int(month) % 10 <= 3:
                quarter = "q1"
            elif 4 <= int(month) % 10 <= 6:
                quarter = "q2"
            elif 7 <= int(month) % 10 <= 9:
                quarter = "q3"
            elif 10 <= int(month) <= 12:
                quarter = "q4"

            company_ticker = file['name'].split("_")[1]
            company_name = companies_ticker_mapping.get(company_ticker, "Not_Listed")

            earnings_call_data = fetch_earnings_call_data(file['name'])

            file_path = "./file.txt"
            destination_blob_name = 'dataset/{}'.format(file['name'])

            write_to_file(file_path, earnings_call_data)
            public_file_url = upload_file_to_gcs(file_path, destination_blob_name)

            delete_file(file_path)

            company_meta_data.append({"company": company_name, "ticker": company_ticker,
                                      "time": datetime.datetime.strptime(year + "-" + month + "-" + date, "%Y-%m-%d"),
                                      "quarter": quarter, "uri": public_file_url})

        batch_key = 'batch_{}'.format(batch_no)
        context['ti'].xcom_push(key=batch_key, value=company_meta_data)

    context['ti'].xcom_push(key='no_of_batches', value=no_of_batches)


def upload_metadata(**context):
    client = get_sql_client(connect_to_sql)

    no_of_batches = context['ti'].xcom_pull(key='no_of_batches')

    for batch_no in range(int(no_of_batches)):
        batch_key = 'batch_{}'.format(batch_no+1)

        data = context['ti'].xcom_pull(key=batch_key)
        df = pd.DataFrame(data)

        with client.connect() as conn:
            df.to_sql(name='earnings_transcript_meta_data', con=conn, index=False, if_exists='append')


#  Create DAG to load data
user_input = {
    "file_upload_batch_size": Param(default=100, type='number'),
}

storage_dag = DAG(
    dag_id="upload_earnings_call_data",
    schedule="0 0 * * *",   # https://crontab.guru/
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["damg7245", "assignment02"],
    params=user_input,
)

with storage_dag:
    upload_files = PythonOperator(
        task_id='upload_files_to_gcs',
        python_callable=upload_files,
        provide_context=True,
        dag=storage_dag
    )

    upload_metadata = PythonOperator(
        task_id='upload_meta_data_to_cloud_sql',
        python_callable=upload_metadata,
        provide_context=True,
        dag=storage_dag
    )

    # Flow
    upload_files >> upload_metadata


table_creation_dag = DAG(
    dag_id="create_table_with_indexes",
    schedule="0 0 * * *",   # https://crontab.guru/
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["damg7245", "assignment02"],
)

with table_creation_dag:
    table_creation = PythonOperator(
        task_id='create_table',
        python_callable=create_table,
        provide_context=True,
        dag=table_creation_dag
    )

    # Flow
    table_creation
