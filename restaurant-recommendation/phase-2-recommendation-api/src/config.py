"""Configuration module for Phase 2 API."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory for Phase 2
BASE_DIR = Path(__file__).parent.parent

# API Configuration
API_VERSION = "v1"
API_TITLE = "Restaurant Recommendation API"
API_DESCRIPTION = "AI-powered restaurant recommendation service"
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '8000'))

# Phase 1 Database Path (relative to Phase 2)
PHASE1_DB_PATH = os.getenv('PHASE1_DB_PATH', '../phase-1-data-pipeline/data/restaurant.db')
PHASE1_DB_FULL_PATH = BASE_DIR / PHASE1_DB_PATH

# Preference Defaults
DEFAULT_MIN_RATING = 0.0
DEFAULT_MAX_PRICE = float('inf')
DEFAULT_LIMIT = 10

# Validation Constraints
MIN_RATING_ALLOWED = 0.0
MAX_RATING_ALLOWED = 5.0
MIN_PRICE_ALLOWED = 0.0
MAX_LIMIT = 100

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
