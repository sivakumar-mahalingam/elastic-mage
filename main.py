import os
import json
import warnings
from elasticsearch import Elasticsearch
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

warnings.filterwarnings('ignore')

# Initialize Elasticsearch client
es = Elasticsearch("https://localhost:9200",
                   basic_auth==("elastic","password"),
                   verify_certs=False)

# Initialize the language model
llm = OpenAI(api_key="your-openai-api-key")

# Define the file path to store the mappings
mappings_file_path = "index_mappings.json"


# Function to get mappings of specified indexes
def get_index_mappings(indexes):
    mappings = {}
    for index in indexes:
        mappings[index] = es.indices.get_mapping(index=index).body
    return mappings


# Function to load mappings from file
def load_mappings_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}


# Function to save mappings to file
def save_mappings_to_file(mappings, file_path):
    with open(file_path, 'w') as file:
        json.dump(mappings, file, indent=4)


# Retrieve and store mappings based on overwrite flag
def retrieve_and_store_mappings(indexes, overwrite=False):
    if not overwrite:
        # Load existing mappings from file if it exists
        mappings = load_mappings_from_file(mappings_file_path)
        if mappings:
            return mappings

    # Fetch mappings from Elasticsearch
    mappings = get_index_mappings(indexes)

    # Save mappings to file
    save_mappings_to_file(mappings, mappings_file_path)
    return mappings


# Example indexes
indexes = ["employee", "employee_personal_detail"]

# Retrieve and store mappings (set overwrite to True to fetch fresh mappings)
mappings = retrieve_and_store_mappings(indexes, overwrite=False)

# Define the prompt template
prompt_template = """
You are an expert Elasticsearch developer, well-versed in the entire Elasticsearch documentation and searching.
Tasked with creating an Elasticsearch query based on the following index mappings.
Mappings:
{mappings}

Convert the following user input into a valid Elasticsearch query:
User Input: "{user_input}"

Ensure the query:
- Is structured to retrieve relevant documents based on the user input.
- Adheres to the mappings provided, using correct Elasticsearch query syntax.
- Generated Elasticsearch query should not contain any index name.
- Strictly consider only the index and field names required.

Elasticsearch Query (in JSON format):
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["mappings", "user_input"])


# Define the query builder function
def build_elasticsearch_query(user_input: str, mappings: dict) -> dict:
    try:
        # Create the sequence using RunnableSequence
        sequence = RunnableSequence(prompt, llm)

        # Generate the query
        es_query = sequence.invoke({"mappings": mappings, "user_input": user_input})

        return eval(es_query)  # Convert the string output to a dictionary
    except Exception as e:
        print(f"Error generating query: {e}")
        return {}


# Example usage
user_input = "Find all documents where the user's age is greater than 30"
mappings_str = {index: json.dumps(mapping) for index, mapping in mappings.items()}

es_query = build_elasticsearch_query(user_input, mappings_str)
print(es_query)

# Execute the query
try:
    # es_query = json.loads(json.dumps(es_query).replace("employee_personal_detail.",""))
    response = es.search(index="employee_personal_detail", body=es_query)
    print(response)
except Exception as e:
    print(f"Error executing query: {e}")
