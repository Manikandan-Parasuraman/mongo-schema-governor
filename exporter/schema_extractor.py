from collections import defaultdict
from exporter.config import SAMPLE_SIZE, MAX_DEPTH, TIMESTAMP_FIELDS_PRIORITY


def get_type(value):
    try:
        return type(value).__name__
    except Exception:
        return "unknown"


def flatten_document(doc, parent_key="", depth=0):
    items = {}

    if depth > MAX_DEPTH:
        return items

    for k, v in doc.items():
        new_key = f"{parent_key}.{k}" if parent_key else k

        if isinstance(v, dict):
            items.update(flatten_document(v, new_key, depth + 1))
        else:
            items[new_key] = get_type(v)

    return items


def detect_timestamp_field(sample_doc):
    for field in TIMESTAMP_FIELDS_PRIORITY:
        if field in sample_doc:
            return field
    return None


def get_latest_cursor(collection, logger):
    try:
        sample_doc = collection.find_one()

        if not sample_doc:
            return collection.find().limit(0)

        ts_field = detect_timestamp_field(sample_doc)

        if ts_field:
            logger.info(f"Using '{ts_field}' for latest data")
            return collection.find().sort(ts_field, -1).limit(SAMPLE_SIZE)

        logger.warning("No timestamp field found, using _id fallback")
        return collection.find().sort("_id", -1).limit(SAMPLE_SIZE)

    except Exception as e:
        logger.error(f"Cursor creation failed: {e}")
        return collection.find().limit(SAMPLE_SIZE)


def infer_schema(collection, logger):
    schema = defaultdict(set)
    total_docs = 0

    try:
        cursor = get_latest_cursor(collection, logger)

        for doc in cursor:
            total_docs += 1
            flat_doc = flatten_document(doc)

            for field, dtype in flat_doc.items():
                schema[field].add(dtype)

    except Exception as e:
        logger.error(f"Schema extraction failed: {e}")

    return {
        "fields": {k: list(v) for k, v in schema.items()},
        "sampled_documents": total_docs,
        "mode": "latest_data"
    }