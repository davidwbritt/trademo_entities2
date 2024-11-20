from typing import Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def merge_documents(
    source_doc: dict[str, Any],
    target_doc: dict[str, Any],
    mapping: dict[str, Any]
) -> dict[str, Any]:
    """
    Merges two JSON documents based on rules defined in the mapping.

    Args:
        source_doc (Dict[str, Any]): The source JSON document.
        target_doc (Dict[str, Any]): The target JSON document.
        mapping (Dict[str, Any]): The mapping JSON defining merge rules.

    Returns:
        Dict[str, Any]: A new dictionary containing the merged document.
    """
    merged_doc = target_doc.copy()

    # Handle 'ignore' rules
    ignore_fields = set(mapping.get("ignore", []))
    if ignore_fields:
        logger.info(f"Ignoring fields: {', '.join(ignore_fields)}")
    

    # Handle 'replace' rules
    replace_fields = mapping.get("replace", [])
    for field in replace_fields:
        if field in source_doc:
            logger.info(f"Replacing field '{field}' from source_doc.")
            merged_doc[field] = source_doc[field]
            
    # Handle 'merge' rules
    merge_fields = mapping.get("merge", [])
    for field in merge_fields:
        if field in source_doc and field in target_doc:
            logger.info(f"Merging field '{field}' from source_doc and target_doc.")
            # Combine lists with deduplication
            if isinstance(source_doc[field], list) and isinstance(target_doc[field], list):
                merged_doc[field] = list(set(target_doc[field] + source_doc[field]))
            # Combine values into a list, ensuring no duplicates
            else:
                merged_values = set(
                    (target_doc[field] if isinstance(target_doc[field], list) else [target_doc[field]])
                    + (source_doc[field] if isinstance(source_doc[field], list) else [source_doc[field]])
                )
                merged_doc[field] = list(merged_values)
        elif field in source_doc:
            merged_doc[field] = source_doc[field]
        elif field in target_doc:
            merged_doc[field] = target_doc[field]
            
            # Add fields from source_doc that are not in target_doc
    for field in source_doc:
        if field not in merged_doc:
            logger.info(f"Adding field '{field}' from source_doc.")
            merged_doc[field] = source_doc[field]

    # Add fields from target_doc that are not in source_doc
    for field in target_doc:
        if field not in merged_doc:
            logger.info(f"Adding field '{field}' from target_doc.")
            merged_doc[field] = target_doc[field]            

    # Remove ignored fields from the merged document
    for field in ignore_fields:
        if field in merged_doc:
            logger.info(f"Removing field '{field}' as per ignore rule.")
            del merged_doc[field]


    return merged_doc
