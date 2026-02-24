"""Configuration module for Phase 1 data pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory for Phase 1
BASE_DIR = Path(__file__).parent.parent

# Database configuration
DB_PATH = os.getenv('DB_PATH', 'data/restaurant.db')
DB_FULL_PATH = BASE_DIR / DB_PATH

# Hugging Face dataset configuration
DATASET_NAME = os.getenv('DATASET_NAME', 'ManikaSaini/zomato-restaurant-recommendation')

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Critical fields that must not be null
CRITICAL_FIELDS = ['name', 'cuisine', 'location', 'rating', 'price']

# Data validation constraints
MIN_RATING = 0.0
MAX_RATING = 5.0
MIN_PRICE = 0
