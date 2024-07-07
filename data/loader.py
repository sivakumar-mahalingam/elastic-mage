import json
from elasticsearch import Elasticsearch, helpers

client = Elasticsearch(
    "https://40ade03392534b2fa513b76bc9e2f258.us-central1.gcp.cloud.es.io:443",
    api_key="ZTZHUmc1QUJxWktHaU5CN2xYWlo6R05YNHY3ZTRRVTIteUNxZEkyRG92QQ=="
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
