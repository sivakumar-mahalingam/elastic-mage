import warnings
import json
import os
from elasticsearch import Elasticsearch
from langchain_community.document_loaders import JSONLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

warnings.filterwarnings('ignore')

es = Elasticsearch(
    "https://40ade03392534b2fa513b76bc9e2f258.us-central1.gcp.cloud.es.io:443",
    api_key="ZTZHUmc1QUJxWktHaU5CN2xYWlo6R05YNHY3ZTRRVTIteUNxZEkyRG92QQ=="
)

mappings_file_path = "index_mappings.json"

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

llm = OpenAI(api_key="sk-proj-6nuCVhND795UGrjQEaq7T3BlbkFJUpKgw1HMa32Rbnz3p76O")


def get_index_mappings(index_pattern):
    map_store = []
    index_mappings = {}

    if index_pattern.lower() == "all":
        indexes = es.indices.get_mapping()
    else:
        indexes = es.indices.get_mapping(index="*" + index_pattern + "*")

    for index, mapping in indexes.items():
        properties = mapping['mappings']['properties']
        cleansed_properties = {key: {"type": value["type"]} for key, value in properties.items()}
        map_store.append({ "index": index, "mappings": cleansed_properties })

    index_mappings = {"map_store": map_store}

    return index_mappings


def load_mappings_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}


def save_mappings_to_file(mappings):
    with open(mappings_file_path, 'w') as file:
        json.dump(mappings, file)


def retrieve_and_store_mappings(index_pattern, overwrite=False):
    if not overwrite:
        index_mappings = load_mappings_from_file(mappings_file_path)
        if index_mappings:
            return index_mappings

    index_mappings = get_index_mappings(index_pattern)

    save_mappings_to_file(index_mappings)

    return index_mappings


def load_retrieve_chroma_rag(index_mappings):
    loader = JSONLoader(file_path=mappings_file_path, jq_schema=".map_store[]", content_key="index", text_content=False)
    documents = loader.load()

    db = Chroma.from_documents(documents, embedding_function)
    retriever = db.as_retriever()

    return retriever


def main():
    index_pattern = input("Enter index pattern (type 'all' for all indexes): ")
    index_mappings = retrieve_and_store_mappings(index_pattern)

    retriever = load_retrieve_chroma_rag(index_mappings)

    template = """You are an expert Elasticsearch developer, well-versed in the entire Elasticsearch.
    Creating an Elasticsearch query based on the index mapping:
    {mapping}
    
    Convert the following user question into a valid Elasticsearch query:
    Question: "{question}"
    
    Ensure the query:
    - Is structured to retrieve relevant documents based on the user input.
    - Adheres to the mappings provided, using correct Elasticsearch query syntax.
    - Generated Elasticsearch query should not contain any index name.
    - Strictly consider only the index names, field names and field type available in index mapping.
    - Always use the exact field names as provided in the index mapping of elasticsearch.
    - Never include details of RAG and vectorstore in elasticsearch query which is returned.
    """

    prompt = PromptTemplate(template=template, input_variables=["mapping", "question"])
    sequence = RunnableSequence(prompt, llm)

    # question = "Find all movies acted by Robert Downey Jr"
    question = "Find all movies which has Gangster in its name"
    es_query = sequence.invoke({"mapping": retriever, "question": question})
    print(es_query)


if __name__ == "__main__":

    main()
