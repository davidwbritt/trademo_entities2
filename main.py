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
from sample import trademo, openc

def main():
    """
    Demonstrates the use of the merge_documents function with example JSON data.
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Mapping rules for merging
    mapping = {
        "replace": ["_id", "name", "jurisdiction"],
        "merge": ["ids", "batch", "address", "url"],
        "preserve-nulls": False
    }

    # Perform the merge
    logger.info("Starting document merge...")
    merged_doc = merge_documents(openc, trademo, mapping)

    # Log the result
    logger.info("Merged Document:\n%s", json.dumps(merged_doc, indent=4))
    
if __name__ == "__main__":
    main()
