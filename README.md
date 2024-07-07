# ElasticMage

ElasticMage is a tool that generates Elasticsearch queries using OpenAI's language models and LangChain. The project dynamically retrieves the index mapping from Elasticsearch, stores it in ChromaDB and uses this mapping to create accurate Elasticsearch queries based on user input questions.

![elastic-mage.png](docs%2Felastic-mage.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project is designed to help developers create valid Elasticsearch queries based on natural language questions. By using OpenAI's GPT-4 model and LangChain, the project converts user questions into structured Elasticsearch queries that adhere to a provided index mapping.

## Features

- Convert natural language questions into Elasticsearch queries.
- Ensure queries adhere to the retrieved index mapping.
- Use OpenAI's powerful language models for accurate query generation.

## Setup

### Prerequisites

- Python 3.7 or higher
- OpenAI API Key
- Elastic instance

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/elasticsearch-query-generator.git
    cd elasticsearch-query-generator
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set your OpenAI API key as an environment variable:

    ```bash
    export OPENAI_API_KEY='your-api-key'
    ```
5. Set your Elasticsearch URL as an environment variable:

    ```bash
    export ELASTICSEARCH_URL='your-elasticsearch-url'
    ```
## Usage

1. Update the `question` variable in `generate_query.py` with your natural language question.

2. Run the script:

    ```bash
    python generate_query.py
    ```

3. The generated Elasticsearch query will be printed in the console.

### Example

Suppose your question is "Find all movies which has Gangster in its name" and your index mapping has a field called `title`. The script should output:

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "title": "Gangster"
          }
        }
      ]
    }
  }
}
```

Reference:
https://python.langchain.com/v0.2/docs/templates/elastic-query-generator/
https://github.com/sckott?tab=repositories
https://docs.pinecone.io/models/overview
https://docs.pinecone.io/examples/notebooks
https://docs.pinecone.io/guides/get-started/quickstart
https://www.pinecone.io/learn/vector-similarity/
https://platform.openai.com/docs/models/gpt-4o
https://platform.openai.com/docs/api-reference/streaming?lang=python

ToDo:
- [ ] Nested ES Schema
- [ ] metadata_func in langchain document loaders
- [ ] Implement RAG