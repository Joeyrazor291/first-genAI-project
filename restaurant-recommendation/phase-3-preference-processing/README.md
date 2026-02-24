# Phase 3: Preference Processing

## Overview

Phase 3 implements the preference processing layer for the AI Restaurant Recommendation Service. This standalone module validates and normalizes user input preferences before they are used for restaurant filtering and recommendation generation.

## Purpose

The preference processor ensures data quality and consistency by:
- Validating user input against defined constraints
- Normalizing text fields (lowercase, trimmed)
- Converting data types appropriately
- Providing clear error messages for invalid inputs
- Applying default values where appropriate
- Generating warnings for unusual but valid inputs

## Architecture Position

This phase sits between the API layer (Phase 2) and the recommendation engine (Phase 5):

```
User Input → API (Phase 2) → Preference Processing (Phase 3) → Database Query → LLM (Phase 4) → Recommendations
```

## Components

### PreferenceProcessor

Main class that handles validation and normalization of user preferences.

**Supported Preferences:**
- `cuisine`: Restaurant cuisine type (string)
- `location`: Restaurant location (string)
- `min_rating`: Minimum rating filter (float, 0.0-5.0)
- `max_price`: Maximum price filter (float, 0.0-10000.0)
- `limit`: Number of results to return (int, 1-100, default: 10)

### ValidationResult

Dataclass that encapsulates validation results:
- `is_valid`: Boolean indicating if validation passed
- `errors`: List of validation error messages
- `warnings`: List of validation warnings
- `normalized_preferences`: Dictionary of normalized preference values

## Validation Rules

### Cuisine
- Must be a string
- Cannot be empty or whitespace-only
- Normalized to lowercase and trimmed
- Unknown cuisines generate warnings but are accepted

### Location
- Must be a string
- Cannot be empty or whitespace-only
- Normalized to lowercase and trimmed

### Min Rating
- Must be numeric (int, float, or numeric string)
- Range: 0.0 to 5.0 (inclusive)
- Converted to float

### Max Price
- Must be numeric (int, float, or numeric string)
- Range: 0.0 to 10000.0 (inclusive)
- Converted to float

### Limit
- Must be an integer or numeric string
- Range: 1 to 100 (inclusive)
- Default: 10 (applied if not provided)
- Converted to int

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Navigate to the phase directory:
```bash
cd restaurant-recommendation/phase-3-preference-processing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from src.preference_processor import PreferenceProcessor

# Initialize processor
processor = PreferenceProcessor()

# Validate and normalize preferences
preferences = {
    'cuisine': 'ITALIAN',
    'location': '  Downtown  ',
    'min_rating': '4.0',
    'max_price': 30,
    'limit': 5
}

result = processor.validate_and_normalize(preferences)

if result.is_valid:
    print("Normalized preferences:", result.normalized_preferences)
    # Output: {'cuisine': 'italian', 'location': 'downtown', 
    #          'min_rating': 4.0, 'max_price': 30.0, 'limit': 5}
else:
    print("Validation errors:", result.errors)

# Check for warnings
if result.warnings:
    print("Warnings:", result.warnings)
```

### Handling Validation Errors

```python
preferences = {
    'cuisine': 'italian',
    'min_rating': 6.0,  # Invalid: > 5.0
    'max_price': -10    # Invalid: negative
}

result = processor.validate_and_normalize(preferences)

if not result.is_valid:
    for error in result.errors:
        print(f"Error: {error}")
    # Output:
    # Error: Rating must be between 0.0 and 5.0, got 6.0
    # Error: Price must be >= 0.0, got -10.0
```

### Applying Defaults

```python
# Apply defaults to normalized preferences
normalized = {'cuisine': 'italian'}
with_defaults = processor.apply_defaults(normalized)

print(with_defaults)
# Output: {'cuisine': 'italian', 'limit': 10}
```

### Getting Filter Summary

```python
# Generate summary for API response
preferences = {
    'cuisine': 'italian',
    'min_rating': 4.0,
    'limit': 10
}

summary = processor.get_filter_summary(preferences)
print(summary)
# Output: {'cuisine': 'italian', 'min_rating': 4.0, 'limit': 10}
```

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Classes

```bash
# Test cuisine validation
pytest tests/test_preference_processor.py::TestCuisineValidation -v

# Test rating validation
pytest tests/test_preference_processor.py::TestRatingValidation -v

# Test edge cases
pytest tests/test_preference_processor.py::TestEdgeCases -v
```

### Test Coverage

The test suite includes 58 comprehensive tests covering:
- ✅ ValidationResult dataclass functionality
- ✅ Cuisine validation and normalization
- ✅ Location validation and normalization
- ✅ Rating validation (boundaries, type conversion, errors)
- ✅ Price validation (boundaries, type conversion, errors)
- ✅ Limit validation (boundaries, defaults, type conversion)
- ✅ Multiple validation errors
- ✅ Default value application
- ✅ Filter summary generation
- ✅ Edge cases (empty dicts, extra fields, unicode, etc.)

All tests pass successfully.

## Project Structure

```
phase-3-preference-processing/
├── src/
│   ├── __init__.py
│   └── preference_processor.py    # Main processor implementation
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Test fixtures
│   └── test_preference_processor.py  # Comprehensive test suite
├── conftest.py                    # Root pytest configuration
├── pytest.ini                     # Pytest settings
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Dependencies

- pytest: Testing framework
- Python standard library (dataclasses, logging, typing)

## Integration with Other Phases

### Phase 2 (API Layer)
Phase 2 receives raw user input and passes it to Phase 3 for validation before querying the database.

```python
# In Phase 2 API endpoint
from phase_3_preference_processing.src.preference_processor import PreferenceProcessor

processor = PreferenceProcessor()
result = processor.validate_and_normalize(user_input)

if not result.is_valid:
    return {"error": result.errors}

# Use result.normalized_preferences for database query
```

### Phase 4 (LLM Integration)
Phase 4 uses the normalized preferences to build context for LLM prompts.

### Phase 5 (Recommendation Engine)
Phase 5 uses validated preferences to filter restaurants and generate recommendations.

## Error Handling

The processor uses a non-exception-based validation approach:
- Returns `ValidationResult` with `is_valid` flag
- Collects all validation errors (not just the first one)
- Provides clear, actionable error messages
- Distinguishes between errors (invalid) and warnings (unusual but valid)

## Future Enhancements

Potential improvements for future iterations:
- Add more cuisine types to the standard list
- Implement location geocoding and validation
- Add support for dietary restrictions
- Add support for price range (min and max)
- Implement fuzzy matching for cuisine names
- Add support for multiple cuisines
- Cache validation results for performance

## Success Criteria

✅ All preference combinations validated correctly  
✅ Graceful handling of missing inputs  
✅ Clear error messages for invalid inputs  
✅ Text normalization (lowercase, trimmed)  
✅ Type conversion (strings to numbers)  
✅ Default values applied appropriately  
✅ 58 comprehensive tests - all passing  
✅ Complete documentation  

## Next Steps

After Phase 3, proceed to:
- **Phase 4**: LLM Integration - Use validated preferences to build prompts
- **Phase 5**: Recommendation Engine - Filter restaurants using normalized preferences
- **Phase 6**: User Interface - Display validation errors to users
- **Phase 7**: Testing & Optimization - End-to-end testing with real user inputs

## License

Part of the AI Restaurant Recommendation Service project.
