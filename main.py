"""
example_merge.py

This script demonstrates the use of the `merge_documents` function from the `merge_docs` module.
It merges two example JSON documents (`source_doc` and `target_doc`) based on specified rules
in a `mapping` JSON.

Usage:
    Run the script directly to see the output of merging the example documents.

Key Features:
    - Replace fields: Overwrite target document values with source document values.
    - Merge fields: Combine values (e.g., lists, dictionaries) from both documents.
    - Logs detailed information about the merge process for easy debugging.
"""

import logging
from merge_docs import merge_documents
import json

def main():
    """
    Demonstrates the use of the merge_documents function with example JSON data.
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Example source and target JSON documents
    source_doc = {
        "name": "Alice Johnson",
        "ids": [10, 20, 30],
        "address": {"city": "San Francisco", "state": "CA"},
        "batch": "batch1",
        "url": "https://example.com/source"
    }

    target_doc = {
        "name": "Bob Smith",
        "ids": [30, 40, 50],
        "address": {"city": "Los Angeles", "state": "CA", "country": "USA"},
        "batch": "batch1",
        "_id": "xyz789",
        "url": "https://example.com/target"
    }

    # Mapping rules for merging
    mapping = {
        "replace": ["name"],
        "merge": ["ids", "batch", "address"],
    }

    # Perform the merge
    logger.info("Starting document merge...")
    merged_doc = merge_documents(source_doc, target_doc, mapping)

    # Log the result
    logger.info("Merged Document:\n%s", json.dumps(merged_doc, indent=4))
    
if __name__ == "__main__":
    main()
