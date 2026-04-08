import os
from dotenv import load_dotenv
from exporter.logger import setup_logger
from exporter.exporter import (
    export_database,
    validate_databases,
    save_output
)


def main():
    load_dotenv()
    logger = setup_logger()

    src_uri = os.getenv("MONGO_URI")
    src_db = os.getenv("MONGO_DB_NAME")

    if not src_uri or not src_db:
        raise ValueError("Source DB config missing")

    tgt_uri = os.getenv("TARGET_MONGO_URI")
    tgt_db = os.getenv("TARGET_DB_NAME")

    source_data = export_database(src_uri, src_db, logger)
    save_output(source_data, "schema_export.json")

    if tgt_uri and tgt_db:
        logger.info("Running validation...")

        target_data = export_database(tgt_uri, tgt_db, logger)
        report = validate_databases(source_data, target_data)

        save_output(report, "validation_report.json")

    else:
        logger.info("Validation skipped")

    logger.info("Completed successfully")


if __name__ == "__main__":
    main()