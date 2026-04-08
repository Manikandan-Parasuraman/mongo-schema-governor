import os
import json
from pymongo import MongoClient
from exporter.config import OUTPUT_DIR, TIMESTAMP
from exporter.schema_extractor import infer_schema
from exporter.index_extractor import extract_indexes
from exporter.validator import compare_schemas, compare_indexes


def connect(uri, logger):
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    logger.info("Connected to MongoDB")
    return client


def ensure_output():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_database(uri, db_name, logger):
    client = connect(uri, logger)
    db = client[db_name]

    data = {}

    try:
        for coll_name in db.list_collection_names():
            logger.info(f"Processing {coll_name}")

            collection = db[coll_name]

            schema = infer_schema(collection, logger)
            indexes = extract_indexes(collection, logger)

            data[coll_name] = {
                "schema": schema,
                "indexes": indexes
            }

    finally:
        client.close()

    return data


def validate_databases(source_data, target_data):
    report = {}

    for coll in source_data:
        if coll not in target_data:
            report[coll] = {"status": "missing_collection"}
            continue

        report[coll] = {
            "schema_diff": compare_schemas(
                source_data[coll]["schema"],
                target_data[coll]["schema"]
            ),
            "index_diff": compare_indexes(
                source_data[coll]["indexes"],
                target_data[coll]["indexes"]
            )
        }

    return report


def save_output(data, filename):
    ensure_output()
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)

    return path