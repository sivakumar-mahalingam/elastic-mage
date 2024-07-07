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

- `Python 3.7 or higher`
- `OpenAI API Key`
- `Elastic instance`

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

4. Create a `.env` file in the root directory to set your OpenAI API key and Elasticsearch details:

    ```bash
    OPENAI_API_KEY='your-api-key'
    ELASTICSEARCH_URL='your-elasticsearch-url'
    ELASTICSEARCH_API_KEY='your-elasticsearch-api-key'
    ```
## Usage

1. Run the script:

    ```bash
    python generate_query.py
    ```

2. Enter index pattern and elastic query needed:

    ```bash
    Enter index pattern (type 'all' for all indexes): omdb
    Enter the kind of elastic query to be formed:Find all movies acted by Robert Downey Jr
    ```

3. The generated Elasticsearch query will be printed in the console.

   ```json
   {
     "query": {
       "bool": {
         "must": {
           "match": {
             "actors": "Robert Downey Jr"
           }
         }
       }
     }
   }
   ```
   Since the question is "Find all movies acted by Robert Downey Jr" and "omdb" index mapping has a field called `actors`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bugs, features, or documentation improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.