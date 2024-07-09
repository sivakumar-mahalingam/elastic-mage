import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

load_dotenv()

client = Elasticsearch(
    os.getenv('ELASTICSEARCH_URL),
    api_key=os.getenv('ELASTICSEARCH_API_KEY')
)

client.info()

with open('omdb.json', 'r') as file:
    try:
        data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        data = []

actions = [
    {
        "_index": "omdb",
        "_source": doc
    }
    for doc in data
]

helpers.bulk(client, actions)
