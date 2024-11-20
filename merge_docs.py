"""
Module to merge two JSON-like dictionaries based on a user-defined mapping.
Supports replace, merge, and ignore rules for fields.
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _deduplicate_dicts(dict_list):
    """
    Deduplicates a list of dictionaries by their content.
    """
    return list({frozenset(item.items()): item for item in dict_list if item is not None}.values())



def _merge_values(source_value, target_value):
    """
    Merges two values, combining lists or handling non-list values.
    """
    if isinstance(source_value, list) and isinstance(target_value, list):
        if all(isinstance(item, dict) for item in source_value + target_value):
            # Deduplicate dictionaries by their content
            return _deduplicate_dicts(source_value + target_value)
        return list(set(filter(None, source_value + target_value)))
    # Handle non-list values
    merged_values = set(
        filter(None, 
            (target_value if isinstance(target_value, list) else [target_value])
            + (source_value if isinstance(source_value, list) else [source_value])
        )
    )
    return next(iter(merged_values)) if len(merged_values) == 1 else list(merged_values)



def merge_documents(source_doc: dict, target_doc: dict, mapping: dict = None) -> dict:
    """
    Merge two dictionaries based on mapping rules.

    Args:
        source_doc (dict): Source dictionary.
        target_doc (dict): Target dictionary.
        mapping (dict, optional): Merge rules (replace, merge, ignore, preserve-nulls).

    Returns:
        dict: Merged dictionary.
    """
    try:
        merged_doc = target_doc.copy()
        mapping = mapping or {}

        # Extract preserve-nulls option
        preserve_nulls = mapping.get("preserve-nulls", True)

        # Handle 'replace' rules
        replace_fields = mapping.get("replace", [])
        for field in replace_fields:
            if field in source_doc:
                logger.info("Replacing field '%s' from source_doc.", field)
                merged_doc[field] = source_doc[field]

        # Handle 'merge' rules
        merge_fields = mapping.get("merge", [])
        for field in merge_fields:
            if field in source_doc and field in target_doc:
                logger.info("Merging field '%s' from source_doc and target_doc.", field)
                merged_doc[field] = _merge_values(
                    source_doc[field], target_doc[field]
                )
            elif field in source_doc:
                merged_doc[field] = source_doc[field]
            elif field in target_doc:
                merged_doc[field] = target_doc[field]

        # Handle 'ignore' rules
        ignore_fields = set(mapping.get("ignore", []))
        if ignore_fields:
            logger.info("Ignoring fields: %s", ", ".join(ignore_fields))
        for field in ignore_fields:
            if field in merged_doc:
                logger.info("Removing field '%s' as per ignore rule.", field)
                del merged_doc[field]

        # Add unique fields from source_doc
        for field in source_doc:
            if field not in merged_doc:
                logger.info("Adding field '%s' from source_doc.", field)
                merged_doc[field] = source_doc[field]

        # Add unique fields from target_doc
        for field in target_doc:
            if field not in merged_doc:
                logger.info("Adding field '%s' from target_doc.", field)
                merged_doc[field] = target_doc[field]

        # Remove null values if preserve-nulls is False
        if not preserve_nulls:
            logger.info("Removing fields with null values as preserve-nulls is False.")
            merged_doc = {key: value for key, value in merged_doc.items() if value is not None}

        return merged_doc

    except KeyError as e:
        logger.error("KeyError encountered: %s", e)
        raise
    except TypeError as e:
        logger.error("TypeError encountered: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise
