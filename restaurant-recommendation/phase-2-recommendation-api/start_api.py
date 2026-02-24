"""Start the API server with proper environment setup."""

import os
import sys
from pathlib import Path

# Set environment variable for database path
db_path = Path(__file__).parent.parent / 'phase-1-data-pipeline' / 'data' / 'restaurant.db'
os.environ['PHASE1_DB_PATH'] = str(db_path.resolve())

print(f"Database path set to: {os.environ['PHASE1_DB_PATH']}")
print()

# Now start uvicorn
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )
