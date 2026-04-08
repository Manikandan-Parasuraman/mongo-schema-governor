Mongo Schema Governor

A production-grade MongoDB governance tool to export latest-data-driven schemas and index definitions, with optional cross-database validation for schema drift detection and consistency enforcement.

Overview

MongoDB is schema-less — but production systems are not.

Mongo Schema Governor helps you:

Infer accurate schema from latest data
Export index definitions
Detect schema drift across environments (dev vs prod)
Support safe data cleanup and migrations
Architecture
                +----------------------+
                |   Source MongoDB     |
                | (Latest Data Only)   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Schema Extractor     |
                | - Latest sampling    |
                | - Nested flattening  |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Index Extractor      |
                | - Unique             |
                | - TTL                |
                | - Partial indexes    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Export Engine        |
                | - JSON output        |
                | - Logging            |
                +----------+-----------+
                           |
                +----------+-----------+
                |                      |
                v                      v
     schema_export.json     validation_report.json
                                      ^
                                      |
                          +-----------+------------+
                          | Target MongoDB (Optional) |
                          +---------------------------+
Features
Core
Latest-data-based schema inference (avoids legacy pollution)
Full index extraction
Nested field detection (user.address.city)
Sampling-based (high performance)
Validation
Cross-database schema comparison
Type mismatch detection
Missing / extra fields detection
Index consistency validation
DevOps Ready
Dockerized
.env driven configuration
Read-only safe execution
Structured logging
Project Structure
mongo-schema-governor/
│
├── exporter/
│   ├── config.py
│   ├── logger.py
│   ├── schema_extractor.py
│   ├── index_extractor.py
│   ├── exporter.py
│   ├── validator.py
│
├── output/
├── .env
├── .env.example
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
Configuration
.env (Minimum Required)
MONGO_URI=mongodb://host.docker.internal:27017
MONGO_DB_NAME=your_source_db
.env (With Validation)
MONGO_URI=mongodb://host.docker.internal:27017
MONGO_DB_NAME=source_db

TARGET_MONGO_URI=mongodb://host.docker.internal:27017
TARGET_DB_NAME=target_db
Usage
Run with Docker (Recommended)
docker-compose up --build
Run Locally
pip install -r requirements.txt
python main.py
Output
1. Schema Export

output/schema_export.json

{
  "users": {
    "schema": {
      "fields": {
        "_id": ["ObjectId"],
        "name": ["str"],
        "email": ["str"],
        "age": ["int", "NoneType"]
      },
      "mode": "latest_data"
    },
    "indexes": [
      {
        "name": "email_1",
        "key": { "email": 1 },
        "unique": true
      }
    ]
  }
}
2. Validation Report (Optional)

output/validation_report.json

{
  "users": {
    "schema_diff": {
      "missing_fields": ["phone"],
      "type_mismatches": [
        {
          "field": "age",
          "source": ["int"],
          "target": ["string"]
        }
      ],
      "new_fields_in_target": ["nickname"]
    },
    "index_diff": {
      "missing_indexes": [],
      "extra_indexes": []
    }
  }
}
How It Works
Schema Extraction
Detects updatedAt → createdAt → _id
Sorts latest documents
Samples recent data
Flattens nested structures
Index Extraction
Uses list_indexes()
Captures:
Unique
Sparse
TTL
Partial indexes
Validation (Optional)

Triggered only if:

TARGET_MONGO_URI
TARGET_DB_NAME

Compares:

Field presence
Data types
Index definitions
Safety Guarantees
No data mutation
Read-only operations
Fallback-safe execution
Per-collection error isolation
Performance
Feature	Behavior
Large collections	Uses sampling
Deep documents	Controlled depth
Failures	Skips and logs
Advanced Configuration (Optional)

Inside config.py:

SAMPLE_SIZE = 1000
MAX_DEPTH = 5
TIMESTAMP_FIELDS_PRIORITY = ["updatedAt", "createdAt"]
Use Cases
Data cleanup preparation
Schema drift detection (dev vs prod)
Migration validation
CI/CD data checks
Index audit
Example Scenarios
Scenario 1: Export Only
# Only source DB configured
docker-compose up

Output:

schema_export.json
Scenario 2: Export + Validate
# Source + target configured
docker-compose up

Output:

schema_export.json
validation_report.json
Roadmap
 Auto-fix schema mismatches
 Index sync (apply missing indexes)
 CI/CD integration (fail on drift)
 Slack / Email alerts
 Schema versioning
Contributing
Fork the repo
Create feature branch
Submit PR
License

MIT License

Final Note

This tool gives you control over MongoDB’s schema chaos — enabling structured, reliable, and production-safe data evolution.