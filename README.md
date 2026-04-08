```markdown
# 🛡️ Mongo Schema Governor

A production-grade MongoDB governance tool designed to export latest-data-driven schemas and index definitions, featuring cross-database validation for schema drift detection and consistency enforcement.

---

## 📖 Overview

MongoDB is schema-less — **but production systems are not.**

Mongo Schema Governor bridges the gap between flexible NoSQL storage and the need for structural integrity. It allows you to:

* **Infer accurate schemas** based on the latest documents (ignoring legacy data debris).
* **Export index definitions** including TTL, Unique, and Partial indexes.
* **Detect schema drift** between environments (e.g., Dev vs. Prod).
* **Facilitate safe migrations** and data cleanup efforts.

---

## 🏗️ Architecture

```text
            +----------------------+
            |   Source MongoDB     |
            | (Latest Data Only)   |
            +----------+-----------+
                       |
                       v
            +----------------------+
            |   Schema Extractor   |
            | - Latest sampling    |
            | - Nested flattening  |
            +----------+-----------+
                       |
                       v
            +----------------------+
            |   Index Extractor    |
            | - Unique & TTL       |
            | - Partial indexes    |
            +----------+-----------+
                       |
                       v
            +----------------------+
            |    Export Engine     |
            | - JSON output        |
            | - Structured Logging |
            +----------+-----------+
                       |
            +----------+-----------+
            |                      |
            v                      v
   schema_export.json     validation_report.json
                                  ^
                                  |
                      +-----------+------------+
                      | Target MongoDB (Opt.)  |
                      +---------------------------+
```

---

## ✨ Features

### 🛠️ Core
* **Latest-Data Inference:** Specifically targets recent records to avoid legacy field pollution.
* **Index Extraction:** Full capture of index properties (Unique, TTL, Sparse).
* **Nested Analysis:** Automatically detects and flattens nested fields (e.g., `user.address.city`).
* **Sampling-Based:** Optimized for performance on large-scale collections.

### 🔍 Validation
* **Cross-DB Comparison:** Compare two databases to find inconsistencies.
* **Type Mismatch Detection:** Alerts you if a field is an `int` in Prod but a `string` in Dev.
* **Field Audit:** Identifies missing or extra fields across environments.

### 🚀 DevOps Ready
* **Dockerized:** Ready for containerized workflows.
* **Environment Driven:** Configured via `.env` files.
* **Read-Only Safe:** Guaranteed not to mutate your production data.

---

## 📂 Project Structure

```text
mongo-schema-governor/
├── exporter/
│   ├── config.py             # Configuration logic
│   ├── logger.py             # Structured logging setup
│   ├── schema_extractor.py   # Schema inference engine
│   ├── index_extractor.py    # MongoDB index logic
│   ├── exporter.py          # Export orchestration
│   └── validator.py         # Schema drift detection
├── output/                   # Generated JSON reports
├── .env                      # Environment variables
├── .env.example              # Template for config
├── main.py                   # Entry point
├── Dockerfile                # Container definition
├── docker-compose.yml        # Orchestration
├── requirements.txt          # Python dependencies
└── README.md
```

---

## ⚙️ Configuration

### 1. Basic Setup (Export Only)
Create a `.env` file in the root directory:
```bash
MONGO_URI=mongodb://host.docker.internal:27017
MONGO_DB_NAME=your_source_db
```

### 2. Validation Setup (Drift Detection)
Add target details to your `.env`:
```bash
MONGO_URI=mongodb://host.docker.internal:27017
MONGO_DB_NAME=source_db

TARGET_MONGO_URI=mongodb://host.docker.internal:27017
TARGET_DB_NAME=target_db
```

---

## 🚀 Usage

### Option 1: Run with Docker (Recommended)
```bash
docker-compose up --build
```

### Option 2: Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Execute the governor
python main.py
```

---

## 📊 Output Examples

### 1. Schema Export (`output/schema_export.json`)
```json
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
```

### 2. Validation Report (`output/validation_report.json`)
```json
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
```

---

## 🧠 How It Works

1.  **Schema Extraction:**
    * Prioritizes sorting by `updatedAt` → `createdAt` → `_id`.
    * Samples the top $N$ documents to define the "current" schema.
    * Flattens dictionaries to dot-notation for deep analysis.
2.  **Index Extraction:**
    * Leverages `list_indexes()` to capture full metadata.
    * Maintains parity for Unique, Sparse, and TTL constraints.
3.  **Safety First:**
    * The tool only uses read operations. 
    * Includes per-collection error isolation to prevent one corrupt collection from stopping the process.

---

## ⚡ Performance & Safety

| Feature | Behavior |
| :--- | :--- |
| **Large Collections** | Uses sampling (default 1000 docs) |
| **Deep Documents** | Controlled depth (default 5 levels) |
| **Data Integrity** | **Read-Only**; no mutations performed |
| **Fault Tolerance** | Skips failing collections and logs errors |

---

## 🗺️ Roadmap

- [ ] **Auto-fix:** Optional scripts to apply missing indexes to Target.
- [ ] **CI/CD Integration:** Fail pipelines if schema drift is detected.
- [ ] **Alerting:** Slack/Email notifications for production drift.
- [ ] **Versioning:** Store historical schema snapshots.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add NewFeature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.
```
