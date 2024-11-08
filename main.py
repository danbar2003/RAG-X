import os
import openai
import numpy as np
import logging
import argparse
from sklearn.metrics.pairwise import cosine_similarity
import extract_symbols


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Set your OpenAI API key
openai.api_key = os.environ.get("KEY")


# Command line interface to get the query from user
def main():
    parser = argparse.ArgumentParser(
        description="Search for a function's code snippet based on a query."
    )
    parser.add_argument(
        "dir_path", help="Path to the directory containing files", default="./"
    )
    parser.add_argument("query", help="The query to search for relevant code")

    args = parser.parse_args()

    symbols_metadata = extract_symbols.extract_symbols_from_directory(args.dir_path)
    snippets = [symbol_metadata["snippet"] for symbol_metadata in symbols_metadata]

    try:
        response = openai.embeddings.create(
            model="text-embedding-3-small", input=snippets
        )
    except Exception as e:
        logging.info("invalid response")
        raise e

    snippets_embeddings = [result.embedding for result in response.data]

    query_embedding = (
        openai.embeddings.create(model="text-embedding-3-small", input=args.query)
        .data[0]
        .embedding
    )

    # Find the cosine similarity between the input text and all other texts
    similarities = cosine_similarity([query_embedding], snippets_embeddings)

    # Get the indices of the top 10 most similar symbols (sorted by similarity score)
    top_10_indices = similarities[0].argsort()[-10:][::-1]  # Sort in descending order

    # Print the top 10 most similar symbols
    for idx in top_10_indices:
        symbol = symbols_metadata[idx]
        print(f"Name: {symbol['name']}")
        print(f"Type: {symbol['type']}")
        print(f"File Path: {symbol['file_path']}")
        print(f"Snippet:\n{symbol['snippet']}\n")
        print("=" * 100)


if __name__ == "__main__":
    main()
