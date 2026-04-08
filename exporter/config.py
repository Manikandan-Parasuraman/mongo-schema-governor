import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
TIMESTAMP = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

SAMPLE_SIZE = 1000
MAX_DEPTH = 5
TIMESTAMP_FIELDS_PRIORITY = ["_id", "updatedAt", "createdAt"]