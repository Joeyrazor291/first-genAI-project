# Phase 1: Data Pipeline - AI Restaurant Recommendation Service

## Purpose and Scope

Phase 1 establishes the foundational data pipeline for the AI Restaurant Recommendation Service. This phase focuses on:

- Fetching restaurant data from the Hugging Face Zomato dataset
- Cleaning and normalizing the data
- Storing the data in a local SQLite database with efficient indexing
- Providing query functions for downstream phases

This phase does NOT include LLM integration, API endpoints, or frontend components. Those will be implemented in subsequent phases.

## Folder Structure

```
phase-1-data-pipeline/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point for the pipeline
│   ├── config.py            # Configuration management
│   └── data/
│       ├── __init__.py
│       ├── ingestion.py     # Dataset loading from Hugging Face
│       ├── preprocessing.py # Data cleaning and normalization
│       └── store.py         # SQLite database operations
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared test fixtures
│   ├── test_ingestion.py    # Tests for data ingestion
│   ├── test_preprocessing.py # Tests for data cleaning
│   └── test_store.py        # Tests for database operations
├── data/
│   └── restaurant.db        # SQLite database (auto-generated)
├── .env                     # Local configuration (not committed)
├── .env.example             # Configuration template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Navigate to the phase-1 directory
cd restaurant-recommendation/phase-1-data-pipeline

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
copy .env.example .env  # Windows
# or
cp .env.example .env    # macOS/Linux

# Edit .env if you need to customize paths or settings
# Default values should work for most cases
```

## Running the Pipeline

### Execute the Full Pipeline

```bash
python src/main.py
```

This will:
1. Load the Zomato restaurant dataset from Hugging Face
2. Clean and normalize the data
3. Store the data in `data/restaurant.db`
4. Print a summary report with statistics and sample queries

### Expected Output

```
================================================================================
PHASE 1: DATA PIPELINE - AI RESTAURANT RECOMMENDATION SERVICE
================================================================================

[STEP 1] Loading dataset from Hugging Face...
INFO - Loading dataset: ManikaSaini/zomato-restaurant-recommendation
INFO - Dataset loaded successfully
INFO - Total records: XXXX
INFO - Columns: [...]

[STEP 2] Cleaning and normalizing data...
INFO - Starting data cleaning. Initial record count: XXXX
INFO - Column names normalized: [...]
INFO - Data cleaning complete. Final record count: XXXX

[STEP 3] Storing data in SQLite database...
INFO - Database initialized at: data/restaurant.db
INFO - Database tables created
INFO - Stored XXXX records in database

================================================================================
PIPELINE SUMMARY REPORT
================================================================================

Data Processing:
  - Total records loaded: XXXX
  - Records after cleaning: XXXX
  - Records removed: XX
  - Retention rate: XX.XX%

Database Statistics:
  - Records stored in DB: XXXX
  - Unique cuisines: XX
  - Unique locations: XX

Sample Query: Top 5 Italian restaurants rated above 4.0
  Found X results:
    1. Restaurant Name - Rating: 4.5, Price: 25.50, Location: downtown
    ...

================================================================================
PHASE 1 PIPELINE COMPLETED SUCCESSFULLY
================================================================================
```

## Running Tests

### Run All Tests

```bash
pytest tests/ -v --tb=short
```

### Run Specific Test Files

```bash
# Test ingestion module
pytest tests/test_ingestion.py -v

# Test preprocessing module
pytest tests/test_preprocessing.py -v

# Test store module
pytest tests/test_store.py -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

## Test Coverage

The test suite covers:

### Ingestion Tests (`test_ingestion.py`)
- Dataset loads without errors
- Loaded data is non-empty
- All expected columns are present
- Handles invalid dataset paths gracefully

### Preprocessing Tests (`test_preprocessing.py`)
- Rows with null critical fields are removed
- Column names normalized to snake_case
- Ratings are floats within 0.0-5.0 range
- Prices are numeric and non-negative
- Cuisine and location values are lowercase and stripped
- Anomalous rows are flagged and excluded
- No duplicate restaurant entries

### Store Tests (`test_store.py`)
- SQLite database created successfully
- Restaurants table exists with correct schema
- Records inserted match DataFrame count
- Filter functions return correct results
- Empty results for no-match queries
- get_all() returns all records
- get_stats() returns correct statistics
- Idempotent writes (no duplicates on re-insert)

## Configuration

The `.env` file supports the following configuration options:

```env
# Database path (relative to phase-1-data-pipeline/)
DB_PATH=data/restaurant.db

# Hugging Face dataset name
DATASET_NAME=ManikaSaini/zomato-restaurant-recommendation

# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
```

## Data Schema

The `restaurants` table in SQLite has the following schema:

| Column   | Type  | Indexed | Description                    |
|----------|-------|---------|--------------------------------|
| id       | INT   | PK      | Auto-incrementing primary key  |
| name     | STR   | No      | Restaurant name                |
| cuisine  | STR   | Yes     | Cuisine type (lowercase)       |
| location | STR   | Yes     | Location (lowercase)           |
| rating   | FLOAT | Yes     | Rating (0.0 - 5.0)            |
| price    | FLOAT | Yes     | Price value                    |

## Query Functions

The `RestaurantStore` class provides the following query functions:

### `filter_restaurants(cuisine, location, min_rating, max_price)`
Filter restaurants by criteria. All parameters are optional.

```python
from src.data.store import RestaurantStore

store = RestaurantStore()
results = store.filter_restaurants(
    cuisine='italian',
    min_rating=4.0,
    max_price=30.0
)
```

### `get_all()`
Retrieve all restaurants from the database.

```python
all_restaurants = store.get_all()
```

### `get_stats()`
Get statistics about the stored data.

```python
stats = store.get_stats()
# Returns: {'total_restaurants': X, 'unique_cuisines': Y, 'unique_locations': Z}
```

## What Phase 2 Will Build

Phase 2 will implement the **Recommendation API** layer, which will:

- Create RESTful API endpoints using FastAPI or Flask
- Implement the Preference Processor to validate user inputs
- Expose query endpoints that use the Phase 1 database
- Add authentication and rate limiting
- Generate OpenAPI documentation

Phase 2 will import and use the `RestaurantStore` class from Phase 1 to query restaurant data.

## Troubleshooting

### Issue: Dataset fails to load
**Solution**: Ensure you have internet connectivity and the Hugging Face dataset URL is correct. Check the dataset exists at: https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation

### Issue: Database file not created
**Solution**: Ensure the `data/` directory exists and you have write permissions. The directory is created automatically, but check file system permissions.

### Issue: Tests fail with import errors
**Solution**: Ensure you're running tests from the `phase-1-data-pipeline/` directory and your virtual environment is activated.

### Issue: Module not found errors
**Solution**: Ensure all `__init__.py` files are present in the directory structure and you've installed all requirements.

## Exit Criteria

Phase 1 is considered complete when:

- ✅ All files exist inside `phase-1-data-pipeline/` with no stray files at project root
- ✅ `python src/main.py` runs end-to-end with no errors
- ✅ Summary report prints with correct record counts and valid sample query results
- ✅ All pytest test cases pass with 0 failures
- ✅ `restaurant.db` is created at `phase-1-data-pipeline/data/restaurant.db`
- ✅ `.env.example` is committed and `.env` is gitignored
- ✅ README.md is complete and accurate
- ✅ Code is modular with single responsibility per file
- ✅ All functions have docstrings

## License

This is part of the AI Restaurant Recommendation Service project.
