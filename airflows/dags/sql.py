import os
from dotenv import load_dotenv

from google.cloud.sql.connector import Connector

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, DateTime, Index

load_dotenv("../../.env")


def connect_to_sql():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/opt/airflow/dags/storage-key.json"  # TODO: for running in local use './storage-key.json'

    return Connector().connect(
        instance_connection_string=os.environ['INSTANCE_CONNECTION_NAME'],
        driver=os.environ["DB_DRIVER"],
        user=os.environ["DB_USER"],
        password=os.environ['DB_PASS'],
        db=os.environ["DB_NAME"]
    )


def get_sql_client(conn):
    return create_engine("postgresql+pg8000://", creator=conn)


# Define the declarative base
Base = declarative_base()


# Define the table schema
class YourTable(Base):
    __tablename__ = 'earnings_transcript_meta_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String(length=60))
    ticker = Column(String(length=10))
    financial_year = Column(DateTime)
    quarter = Column(String(length=3))
    uri = Column(String(length=255))

    # Define indexes on columns
    index1 = Index('company_idx', company)
    index2 = Index('company_data_idx', financial_year, company)


def create_table():
    client = get_sql_client(connect_to_sql)

    with client.connect() as conn:
        # Create the table
        Base.metadata.create_all(conn)

        conn.close()


def insert_to_table(engine, table_name, data):
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Define the metadata
    metadata = MetaData(bind=engine)

    table = Table(table_name, metadata, autoload=True, autoload_with=engine)

    # Create an insert statement
    stmt = table.insert().values(data)

    # Execute the insert statement
    session.execute(stmt)

    # Commit the transaction
    session.commit()

    # Close the session
    session.close()
