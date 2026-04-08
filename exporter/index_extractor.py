def extract_indexes(collection, logger):
    indexes = []

    try:
        for idx in collection.list_indexes():
            indexes.append({
                "name": idx.get("name"),
                "key": dict(idx.get("key")),
                "unique": idx.get("unique", False),
                "sparse": idx.get("sparse", False),
                "ttl": idx.get("expireAfterSeconds"),
                "partialFilterExpression": idx.get("partialFilterExpression")
            })

    except Exception as e:
        logger.error(f"Index extraction failed: {e}")

    return indexes