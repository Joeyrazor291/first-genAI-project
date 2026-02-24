# Phase 6: Frontend Interface

Simple HTML/CSS/JavaScript frontend for the AI Restaurant Recommendation Service.

## Overview

This phase provides a user-friendly web interface that connects to the Phase 2 API to deliver restaurant recommendations. The frontend is built with vanilla JavaScript (no build tools required) and features a modern, responsive design.

## Features

- **Preference Form**: Easy-to-use form for entering dining preferences
  - Cuisine type filtering
  - Location filtering
  - Minimum rating threshold
  - Maximum price limit
  - Configurable result count

- **Real-time API Status**: Health check indicator showing API availability

- **Recommendation Display**: Beautiful cards showing:
  - Restaurant name and ranking
  - Cuisine types and location
  - Rating with star visualization
  - Price information
  - AI-generated explanation
  - Full address

- **User Experience**:
  - Loading states with animations
  - Error handling with clear messages
  - Responsive design (mobile-friendly)
  - Smooth scrolling and transitions
  - Filter tags showing active preferences

## Prerequisites

1. **Phase 2 API must be running**:
   ```bash
   cd ../phase-2-recommendation-api
   python -m uvicorn src.main:app --reload
   ```

2. **Phase 1 Database must exist**:
   - Located at `../phase-1-data-pipeline/data/restaurant.db`

3. **Phase 5 Recommendation Engine must be configured**:
   - Groq API key in Phase 4 `.env` file

## Setup

### Option 1: Python HTTP Server (Recommended)

1. Navigate to the frontend directory:
   ```bash
   cd restaurant-recommendation/phase-6-frontend
   ```

2. Start a simple HTTP server:
   ```bash
   # Python 3
   python -m http.server 8080
   
   # Or Python 2
   python -m SimpleHTTPServer 8080
   ```

3. Open your browser:
   ```
   http://localhost:8080
   ```

### Option 2: Node.js HTTP Server

1. Install http-server globally (if not already installed):
   ```bash
   npm install -g http-server
   ```

2. Start the server:
   ```bash
   http-server -p 8080
   ```

3. Open your browser:
   ```
   http://localhost:8080
   ```

### Option 3: Direct File Access

Simply open `index.html` in your browser. Note: Some browsers may restrict API calls from `file://` protocol due to CORS policies.

## Usage

1. **Start the Backend API**:
   ```bash
   cd ../phase-2-recommendation-api
   python -m uvicorn src.main:app --reload
   ```
   The API will run on `http://localhost:8000`

2. **Open the Frontend**:
   - Navigate to `http://localhost:8080` (or your chosen port)

3. **Enter Your Preferences**:
   - Fill in any combination of filters (all are optional except limit)
   - Click "Get Recommendations"

4. **View Results**:
   - See personalized recommendations with AI explanations
   - Review restaurant details, ratings, and prices

## Configuration

### API Base URL

If your API runs on a different port or host, update the configuration in `app.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';  // Change this
const API_VERSION = 'v1';
```

### CORS Settings

The Phase 2 API is configured to allow all origins. If you need to restrict this, update the CORS middleware in `../phase-2-recommendation-api/src/api.py`.

## File Structure

```
phase-6-frontend/
├── index.html          # Main HTML structure
├── styles.css          # Complete styling and animations
├── app.js             # JavaScript for API integration
└── README.md          # This file
```

## API Endpoints Used

The frontend interacts with these Phase 2 API endpoints:

1. **Health Check**: `GET /health`
   - Checks API and engine availability
   - Updates status indicator

2. **Get Recommendations**: `POST /api/v1/recommendations`
   - Sends user preferences
   - Receives personalized recommendations

3. **Get Stats**: `GET /api/v1/stats` (optional)
   - Database statistics
   - Can be added to UI if needed

## Features in Detail

### Form Validation

- Client-side validation for all inputs
- Rating: 0.0 - 5.0
- Price: Must be positive
- Limit: 1 - 100
- Clear error messages for invalid inputs

### Loading States

- Button shows spinner during API calls
- Full-page loading indicator
- Prevents duplicate submissions

### Error Handling

- Network errors
- API errors
- Validation errors
- No results found
- Clear, user-friendly messages

### Responsive Design

- Mobile-first approach
- Adapts to all screen sizes
- Touch-friendly interface
- Optimized for tablets and phones

## Troubleshooting

### API Status Shows "Offline"

1. Verify Phase 2 API is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check if the API port matches `app.js` configuration

3. Ensure CORS is enabled in the API

### No Recommendations Found

1. Try broader filters (remove some constraints)
2. Check if Phase 1 database has data
3. Verify Phase 5 engine is initialized

### CORS Errors

1. Ensure Phase 2 API has CORS middleware enabled
2. Don't use `file://` protocol - use HTTP server
3. Check browser console for specific CORS errors

## Testing

### Manual Testing Checklist

- [ ] API status indicator shows "Online"
- [ ] Form accepts valid inputs
- [ ] Form rejects invalid inputs (rating > 5, negative price)
- [ ] Loading state appears during API call
- [ ] Recommendations display correctly
- [ ] Filter tags show active preferences
- [ ] Error messages display for failures
- [ ] Responsive design works on mobile
- [ ] All links and buttons work

### Test Scenarios

1. **All Filters**: Enter all preferences and verify results
2. **No Filters**: Leave all optional fields empty
3. **Invalid Input**: Try rating = 10, verify error
4. **No Results**: Enter impossible criteria (e.g., rating = 5.0, max_price = 1)
5. **API Down**: Stop the API and verify error handling

## Future Enhancements

Potential improvements for future versions:

- [ ] Save favorite restaurants
- [ ] User authentication
- [ ] Restaurant details modal
- [ ] Map integration
- [ ] Filter presets
- [ ] Search history
- [ ] Share recommendations
- [ ] Dark mode toggle
- [ ] Advanced filters (delivery, outdoor seating, etc.)
- [ ] Sort options (by rating, price, distance)

## Architecture Integration

This frontend completes the full stack:

```
User Browser (Phase 6)
    ↓
FastAPI REST API (Phase 2)
    ↓
Recommendation Engine (Phase 5)
    ↓
├── Preference Processor (Phase 3)
├── LLM Service (Phase 4)
└── Database Service (Phase 1)
```

## Support

For issues or questions:
1. Check Phase 2 API logs
2. Verify all phases are properly configured
3. Review browser console for JavaScript errors
4. Ensure database exists and has data

## License

Part of the AI Restaurant Recommendation Service project.
