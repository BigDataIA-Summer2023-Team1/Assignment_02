# diagram.py
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.gcp.storage import Storage
from diagrams.gcp.database import SQL
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.vcs import Github
from diagrams.custom import Custom
from urllib.request import urlretrieve

with Diagram("Summarization Engine", show=False, filename="arch_diagram", direction="LR"):

    cc_streamlit = Custom("Streamlit", "./images/streamlit.png")
    cc_langchain = Custom("Langchain", "./images/langchain.png")
    cc_pinecone = Custom("Pinecone", "./images/pinecone.png")

    [Github("MetaData"),Github("Earnings data")] >> Airflow("airflow") >> [SQL("Meta Data"),Storage("File")] >> cc_streamlit
    

    cc_langchain >> cc_streamlit
    cc_streamlit >> cc_langchain
    cc_pinecone >> cc_langchain  
    


    # cc_heart = Custom("Creative Commons", "./images/cc_heart.black.png")
    # cc_attribution = Custom("Credit must be given to the creator", "./images/cc_attribution.png")

    # cc_sa = Custom("Adaptations must be shared\n under the same terms", "./images/cc_sa.png")
    # cc_nd = Custom("No derivatives or adaptations\n of the work are permitted", "./images/cc_nd.png")
    # cc_zero = Custom("Public Domain Dedication", "./images/cc_zero.png")

    # cc_heart >> cc_attribution
    # cc_heart >> cc_sa
    # cc_heart >> cc_nd
    # cc_heart >> cc_zero