# Design Document: Phase 6 React Migration

## Overview

This design document outlines the architecture and implementation approach for migrating the Phase 6 frontend from vanilla JavaScript to React 18+. The migration maintains 100% feature parity with the existing implementation while modernizing the codebase with functional components, hooks, and Tailwind CSS.

The React application will be structured as a collection of modular, reusable components that manage their own state using hooks. All styling will be converted from the current CSS file to Tailwind CSS utility classes. The API integration layer will remain functionally identical, preserving all communication patterns with the Phase 2 backend.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Application                         │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              App Component (Root)                     │   │
│  │  - Manages global state (recommendations, errors)    │   │
│  │  - Handles API health check on mount                 │   │
│  │  - Coordinates component communication               │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                   │
│        ┌──────────────────┼──────────────────┐               │
│        │                  │                  │               │
│  ┌─────▼──────┐  ┌────────▼────────┐  ┌─────▼──────┐       │
│  │   Header   │  │  PreferenceForm │  │   Footer   │       │
│  │ Component  │  │   Component     │  │ Component  │       │
│  └────────────┘  └────────┬────────┘  └────────────┘       │
│                           │                                   │
│                  ┌────────▼────────┐                         │
│                  │  Results Section │                         │
│                  │  - Filter Tags   │                         │
│                  │  - Results Info  │                         │
│                  │  - Cards Grid    │                         │
│                  └────────┬────────┘                         │
│                           │                                   │
│        ┌──────────────────┼──────────────────┐               │
│        │                  │                  │               │
│  ┌─────▼──────────┐  ┌────▼─────┐  ┌────────▼────┐         │
│  │ Loading State  │  │   Error   │  │ Recommend.  │         │
│  │  Component     │  │ Component │  │ Card List   │         │
│  └────────────────┘  └───────────┘  └─────────────┘         │
│                                             │                 │
│                                    ┌────────▼────────┐       │
│                                    │ Recommendation  │       │
│                                    │ Card Component  │       │
│                                    │ (Reusable)      │       │
│                                    └─────────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTP/REST
                           │
                    ┌──────▼──────┐
                    │  Phase 2 API │
                    │  (Backend)   │
                    └──────────────┘
```

### Component Hierarchy

```
App
├── Header
├── PreferenceForm
│   └── FormInputs (cuisine, location, rating, price, limit)
├── LoadingState
├── ErrorMessage
├── ResultsSection
│   ├── ResultsHeader
│   │   ├── Title
│   │   └── ResultsInfo
│   ├── FilterTags
│   └── RecommendationsList
│       └── RecommendationCard (repeated)
└── Footer
    └── APIHealthCheck
```

## Components and Interfaces

### 1. App Component (Root)

**Purpose**: Main application component that orchestrates all child components and manages global state.

**State**:
- `preferences`: Object containing user-entered preferences
- `recommendations`: Array of recommendation objects from API
- `loading`: Boolean indicating if API request is in progress
- `error`: String containing error message or null
- `apiStatus`: String indicating API health ('online', 'offline', 'degraded')
- `resultsInfo`: Object containing count and total_found from API response
- `filtersApplied`: Object containing active filters from API response

**Effects**:
- On mount: Call `checkAPIHealth()` to verify backend availability
- On preferences change: Clear previous results and errors

**Methods**:
- `checkAPIHealth()`: Fetch `/health` endpoint and update apiStatus
- `handleFormSubmit(preferences)`: Validate and submit preferences to API
- `fetchRecommendations(preferences)`: POST to `/api/v1/recommendations`
- `clearResults()`: Reset recommendations and errors

**Props**: None (root component)

**Children**: Header, PreferenceForm, LoadingState, ErrorMessage, ResultsSection, Footer

---

### 2. Header Component

**Purpose**: Display application title and subtitle.

**State**: None

**Props**: None

**Rendering**:
- Title: "🍽️ AI Restaurant Recommendations"
- Subtitle: "Find your perfect dining experience"

**Styling**: Gradient background (purple), white text, centered

---

### 3. PreferenceForm Component

**Purpose**: Collect user dining preferences through form inputs.

**State**:
- `formData`: Object containing all form field values
  - `cuisine`: String
  - `location`: String
  - `minRating`: Number or empty string
  - `maxPrice`: Number or empty string
  - `limit`: Number (default: 5)

**Props**:
- `onSubmit`: Callback function receiving preferences object
- `isLoading`: Boolean indicating if submission is in progress

**Methods**:
- `handleInputChange(fieldName, value)`: Update form state
- `validateForm()`: Validate all inputs before submission
- `handleSubmit(event)`: Prevent default, validate, and call onSubmit

**Validation Rules**:
- `minRating`: Must be between 0 and 5 (if provided)
- `maxPrice`: Must be positive (if provided)
- `limit`: Must be between 1 and 100 (required, default 5)
- `cuisine`: Optional, any string
- `location`: Optional, any string

**Rendering**:
- Form with 5 input fields in responsive grid
- Submit button with loading state
- Helper text under each field

---

### 4. LoadingState Component

**Purpose**: Display loading feedback during API requests.

**Props**:
- `isVisible`: Boolean indicating if loading state should display

**Rendering**:
- Spinner animation (rotating circle)
- Message: "Finding the best restaurants for you..."
- Full-page overlay effect

**Styling**: Centered, with large spinner and descriptive text

---

### 5. ErrorMessage Component

**Purpose**: Display error messages to users.

**Props**:
- `message`: String containing error message
- `isVisible`: Boolean indicating if error should display

**Methods**:
- `scrollIntoView()`: Auto-scroll error into view when displayed

**Rendering**:
- Error message text with icon
- Red background with left border
- Supports multi-line messages

---

### 6. ResultsSection Component

**Purpose**: Container for displaying recommendations and related information.

**Props**:
- `recommendations`: Array of recommendation objects
- `resultsInfo`: Object with count and total_found
- `filtersApplied`: Object with active filters
- `warnings`: Array of warning messages (if any)

**Children**:
- ResultsHeader (title + info)
- FilterTags (active filters)
- RecommendationsList (grid of cards)

**Rendering**: Only displays when recommendations exist

---

### 7. FilterTags Component

**Purpose**: Display active filters as visual tags.

**Props**:
- `filtersApplied`: Object with active filters
- `warnings`: Array of warning messages

**Rendering**:
- Blue background container
- Individual tags for each active filter
- Warning messages if present

**Styling**: Inline tags with rounded corners, blue theme

---

### 8. ResultsInfo Component

**Purpose**: Display count information about results.

**Props**:
- `totalFound`: Number of restaurants found
- `showing`: Number of recommendations being displayed

**Rendering**:
- "Found X restaurant(s)"
- "Showing Y"

**Styling**: Small text, secondary color

---

### 9. RecommendationsList Component

**Purpose**: Container for displaying recommendation cards in a grid.

**Props**:
- `recommendations`: Array of recommendation objects

**Rendering**:
- Responsive grid layout (1 column on mobile, 2-3 on desktop)
- RecommendationCard component for each item
- Staggered fade-in animation

---

### 10. RecommendationCard Component

**Purpose**: Display individual restaurant recommendation.

**Props**:
- `restaurant`: Object containing restaurant data
- `explanation`: String with AI-generated explanation
- `rank`: Number indicating ranking position

**Data Mapping** (handles both old and new API formats):
- `name`: restaurant.name || restaurant.restaurant_name
- `cuisine`: restaurant.cuisine || restaurant.cuisines
- `location`: restaurant.location || restaurant.locality || restaurant.city
- `rating`: restaurant.rating || restaurant.aggregate_rating
- `price`: restaurant.price || restaurant.average_cost_for_two
- `address`: restaurant.address (optional)

**Rendering**:
- Rank badge (#1, #2, etc.)
- Restaurant name (large, bold)
- Cuisine and location (with icons)
- Rating with star visualization
- Price information
- AI explanation in highlighted box
- Address (if available)

**Styling**: Card with border, hover effect (elevation), responsive

---

### 11. Footer Component

**Purpose**: Display footer information and API status.

**Props**:
- `apiStatus`: String ('online', 'offline', 'degraded')

**Rendering**:
- "Powered by AI • Built with ❤️"
- API Status indicator with color coding
- Link to debug page

**Styling**: Secondary background, centered text

---

### 12. APIHealthCheck Component

**Purpose**: Display real-time API availability status.

**Props**:
- `status`: String ('online', 'offline', 'degraded')

**Rendering**:
- Status text with colored indicator badge
- Green for online, red for offline, yellow for degraded

**Styling**: Inline badge with appropriate color

---

## Data Models

### Preferences Object

```javascript
{
  cuisine?: string,           // Optional: cuisine type
  location?: string,          // Optional: location
  min_rating?: number,        // Optional: 0.0 - 5.0
  max_price?: number,         // Optional: positive number
  limit: number               // Required: 1 - 100
}
```

### Recommendation Object (from API)

```javascript
{
  restaurant: {
    name: string,
    cuisine: string,
    location: string,
    rating: number,
    price: number,
    address?: string
  },
  explanation: string
}
```

### API Response Object

```javascript
{
  success: boolean,
  count: number,
  total_found: number,
  recommendations: Recommendation[],
  filters_applied: {
    cuisine?: string,
    location?: string,
    min_rating?: number,
    max_price?: number
  },
  warnings?: string[]
}
```

### API Health Response

```javascript
{
  status: 'healthy' | 'degraded' | 'unhealthy',
  timestamp: string,
  details?: object
}
```

## Styling Strategy

### Tailwind CSS Approach

All styling will be implemented using Tailwind CSS utility classes. The visual appearance will be identical to the current CSS implementation.

**Color Palette**:
- Primary: Blue (#2563eb)
- Success: Green (#10b981)
- Error: Red (#ef4444)
- Warning: Amber (#f59e0b)
- Text Primary: Gray-900 (#1f2937)
- Text Secondary: Gray-600 (#6b7280)
- Background Primary: White (#ffffff)
- Background Secondary: Gray-50 (#f9fafb)
- Border: Gray-200 (#e5e7eb)

**Responsive Breakpoints**:
- Mobile: < 768px (single column layouts)
- Tablet: 768px - 1024px (2 column layouts)
- Desktop: > 1024px (3+ column layouts)

**Key Styling Areas**:
- Header: Gradient background, large typography
- Form: Grid layout with responsive columns
- Cards: Hover effects, shadows, transitions
- Loading: Spinner animation
- Errors: Red background with left border
- Buttons: Primary color with hover state

## State Management with Hooks

### useState Hooks

1. **Preferences State**
   ```javascript
   const [preferences, setPreferences] = useState({
     cuisine: '',
     location: '',
     minRating: '',
     maxPrice: '',
     limit: 5
   });
   ```

2. **Recommendations State**
   ```javascript
   const [recommendations, setRecommendations] = useState([]);
   ```

3. **Loading State**
   ```javascript
   const [loading, setLoading] = useState(false);
   ```

4. **Error State**
   ```javascript
   const [error, setError] = useState(null);
   ```

5. **API Status State**
   ```javascript
   const [apiStatus, setApiStatus] = useState('checking');
   ```

6. **Results Info State**
   ```javascript
   const [resultsInfo, setResultsInfo] = useState(null);
   ```

7. **Filters Applied State**
   ```javascript
   const [filtersApplied, setFiltersApplied] = useState(null);
   ```

### useEffect Hooks

1. **API Health Check on Mount**
   ```javascript
   useEffect(() => {
     checkAPIHealth();
   }, []);
   ```

2. **Clear Results on New Submission**
   ```javascript
   useEffect(() => {
     setRecommendations([]);
     setError(null);
   }, [preferences]);
   ```

### useCallback Hooks

1. **Memoized Form Submit Handler**
   ```javascript
   const handleFormSubmit = useCallback((newPreferences) => {
     // Validation and API call
   }, []);
   ```

2. **Memoized API Health Check**
   ```javascript
   const checkAPIHealth = useCallback(async () => {
     // API call
   }, []);
   ```

## API Integration

### Endpoints Used

1. **Health Check**
   - Method: GET
   - URL: `{API_BASE_URL}/health`
   - Response: `{ status: 'healthy' | 'degraded' | 'unhealthy', ... }`

2. **Get Recommendations**
   - Method: POST
   - URL: `{API_BASE_URL}/api/v1/recommendations`
   - Request Body: Preferences object
   - Response: API Response object with recommendations array

### Error Handling

- Network errors: Display "Unable to connect to API"
- Validation errors: Display specific validation message
- API errors: Extract and display error.detail.error or error.detail
- No results: Display helpful suggestions based on applied filters

### Configuration

- `API_BASE_URL`: Configurable constant (default: 'http://localhost:8000')
- `API_VERSION`: Constant (default: 'v1')

## File Structure

```
src/
├── App.jsx                          # Root component
├── components/
│   ├── Header.jsx                   # Header component
│   ├── PreferenceForm.jsx           # Form component
│   ├── LoadingState.jsx             # Loading indicator
│   ├── ErrorMessage.jsx             # Error display
│   ├── ResultsSection.jsx           # Results container
│   ├── FilterTags.jsx               # Filter tags display
│   ├── ResultsInfo.jsx              # Results count info
│   ├── RecommendationsList.jsx      # Cards grid
│   ├── RecommendationCard.jsx       # Individual card
│   ├── Footer.jsx                   # Footer component
│   └── APIHealthCheck.jsx           # API status indicator
├── hooks/
│   ├── usePreferences.js            # Custom hook for preferences
│   ├── useRecommendations.js        # Custom hook for recommendations
│   └── useAPIHealth.js              # Custom hook for API health
├── services/
│   └── api.js                       # API communication functions
├── styles/
│   └── globals.css                  # Tailwind imports and globals
├── index.jsx                        # React entry point
└── index.html                       # HTML template
```

## Error Handling Strategy

### Validation Errors

- Client-side validation before API submission
- Clear error messages for each field
- Prevent form submission on validation failure

### API Errors

- Catch network errors and display connection message
- Parse API error responses and display user-friendly messages
- Provide suggestions for common error scenarios

### No Results

- Detect when count === 0
- Display message with filter adjustment suggestions
- Reference debug page for available options

### Recovery

- Allow users to modify preferences and resubmit
- Clear previous errors when new request is made
- Maintain form state for easy adjustment

## Performance Considerations

### Optimization Techniques

1. **Component Memoization**: Use React.memo for RecommendationCard to prevent unnecessary re-renders
2. **Callback Memoization**: Use useCallback for event handlers to maintain referential equality
3. **Lazy Loading**: Consider lazy loading recommendation cards if list becomes very large
4. **Debouncing**: Debounce form input changes if real-time validation is added

### Bundle Size

- Use production build for deployment
- Tree-shake unused Tailwind CSS utilities
- Minimize JavaScript bundle size

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- React 18+ requirements
- ES6+ JavaScript support
- CSS Grid and Flexbox support

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.


### Correctness Properties

Based on the acceptance criteria analysis, the following properties define the expected behavior of the React application:

#### Property 1: Form Input Acceptance and Storage
*For any* text input in the cuisine or location fields, the form should accept and store the value without modification.
**Validates: Requirements 2.2, 2.3**

#### Property 2: Rating Validation
*For any* numeric input in the minimum rating field, the form should accept values between 0.0 and 5.0 (inclusive) and reject values outside this range.
**Validates: Requirements 2.4**

#### Property 3: Price Validation
*For any* numeric input in the maximum price field, the form should accept positive values and reject negative or zero values.
**Validates: Requirements 2.5**

#### Property 4: Limit Validation
*For any* numeric input in the result limit field, the form should accept values between 1 and 100 (inclusive) and reject values outside this range, with a default value of 5.
**Validates: Requirements 2.6**

#### Property 5: Form Submission Prevention on Invalid Input
*For any* invalid input combination (rating > 5, price < 0, limit < 1 or > 100), form submission should be prevented and an error message should be displayed.
**Validates: Requirements 2.7, 2.8**

#### Property 6: API Request Triggering
*For any* valid preference submission, an HTTP POST request should be triggered to the `/api/v1/recommendations` endpoint with the user preferences as the request body.
**Validates: Requirements 2.9, 9.2**

#### Property 7: API Health Check on Mount
*For any* application initialization, a GET request should be made to the `/health` endpoint to check API availability.
**Validates: Requirements 3.1, 9.1**

#### Property 8: API Status Display - Online
*For any* successful API health check response with status 'healthy', the API_Health_Check component should display "Online" with a green indicator.
**Validates: Requirements 3.2**

#### Property 9: API Status Display - Offline
*For any* failed API health check (network error or non-healthy response), the API_Health_Check component should display "Offline" with a red indicator.
**Validates: Requirements 3.3**

#### Property 10: API Status Display - Degraded
*For any* API health check response with status 'degraded', the API_Health_Check component should display "Degraded" with a yellow indicator.
**Validates: Requirements 3.4**

#### Property 11: Recommendation Card Rendering
*For any* recommendation object from the API response, a RecommendationCard component should be rendered displaying the restaurant data.
**Validates: Requirements 4.1**

#### Property 12: Recommendation Card Content - Basic Info
*For any* recommendation card, the rendered output should contain the restaurant name, cuisine type, and location.
**Validates: Requirements 4.2**

#### Property 13: Recommendation Card Content - Rating and Price
*For any* recommendation card, the rendered output should contain the rating value and price information.
**Validates: Requirements 4.3**

#### Property 14: Recommendation Card Content - Explanation
*For any* recommendation card, the rendered output should contain the AI-generated explanation text.
**Validates: Requirements 4.4**

#### Property 15: Recommendation Card Content - Address
*For any* recommendation card where address data is available, the rendered output should contain the address; if address is not available, the card should render without errors.
**Validates: Requirements 4.5**

#### Property 16: Recommendation Card Ranking
*For any* recommendation card at position N in the recommendations list, the card should display the ranking number N.
**Validates: Requirements 4.6**

#### Property 17: Loading State Display
*For any* API request in progress, the LoadingState component should be visible displaying a spinner animation and a message.
**Validates: Requirements 5.1, 5.2**

#### Property 18: Button Disabled During Loading
*For any* API request in progress, the submit button should be disabled and display a loading indicator.
**Validates: Requirements 5.3**

#### Property 19: Loading State Removal
*For any* completed API request (success or failure), the LoadingState component should be hidden and the submit button should be re-enabled.
**Validates: Requirements 5.4, 5.5**

#### Property 20: Error Message Display on API Failure
*For any* API request failure, an error message should be displayed to the user describing the error.
**Validates: Requirements 6.1**

#### Property 21: Error Message Display on Validation Failure
*For any* form validation failure, an error message should be displayed describing the specific validation error.
**Validates: Requirements 6.2**

#### Property 22: Error Message Display on No Results
*For any* API response with zero recommendations, an error message should be displayed with helpful suggestions for adjusting filters.
**Validates: Requirements 6.3**

#### Property 23: Error Message Auto-Scroll
*For any* error message display, the error component should scroll into view automatically.
**Validates: Requirements 6.4**

#### Property 24: Error Message Clearing
*For any* new form submission, any previously displayed error messages should be cleared.
**Validates: Requirements 6.5**

#### Property 25: Filter Tags Display
*For any* active filter in the API response, a corresponding filter tag should be displayed showing the filter name and value.
**Validates: Requirements 7.1, 7.3**

#### Property 26: Filter Tags Exclusion
*For any* inactive filter (not in the filters_applied response), no tag should be displayed for that filter.
**Validates: Requirements 7.2**

#### Property 27: Filter Tags Visibility
*For any* API response with no active filters (empty filters_applied object), the FilterTags component should not be displayed.
**Validates: Requirements 7.4**

#### Property 28: Results Count Display
*For any* API response with recommendations, the results information should display the total_found count.
**Validates: Requirements 8.1**

#### Property 29: Results Showing Count
*For any* API response with recommendations, the results information should display the count of recommendations being shown.
**Validates: Requirements 8.2**

#### Property 30: Pluralization
*For any* count value N, the results information should use "restaurant" when N=1 and "restaurants" when N≠1.
**Validates: Requirements 8.3**

#### Property 31: Content-Type Header
*For any* API request made by the application, the Content-Type header should be set to 'application/json'.
**Validates: Requirements 9.3**

#### Property 32: API Response Parsing
*For any* successful API response, the application should correctly parse the JSON and extract all recommendation data without errors.
**Validates: Requirements 9.4**

#### Property 33: API Error Extraction
*For any* API error response, the application should extract the error message from error.detail.error or error.detail and display it to the user.
**Validates: Requirements 9.5**

#### Property 34: Form Input Validation
*For any* input type (text, number), the form should accept valid inputs and reject invalid inputs with appropriate error messages.
**Validates: Requirements 15.1**

#### Property 35: API Status Correctness
*For any* API health check response, the displayed status should match the actual API response status.
**Validates: Requirements 15.2**

#### Property 36: Multiple Submissions
*For any* sequence of form submissions, each submission should trigger a new API request and display new results without errors or state corruption.
**Validates: Requirements 16.5**

#### Property 37: Recommendation Details Completeness
*For any* recommendation displayed in the results, all required fields (name, cuisine, location, rating, price, explanation) should be present in the rendered output.
**Validates: Requirements 16.4**

## Error Handling

### Error Categories

1. **Validation Errors**
   - Invalid rating (< 0 or > 5)
   - Invalid price (< 0)
   - Invalid limit (< 1 or > 100)
   - Empty required fields

2. **Network Errors**
   - Connection refused
   - Timeout
   - DNS resolution failure

3. **API Errors**
   - 400 Bad Request (invalid preferences)
   - 500 Internal Server Error
   - 503 Service Unavailable

4. **Data Errors**
   - Missing required fields in response
   - Invalid data types
   - Malformed JSON

### Error Recovery

- Display user-friendly error messages
- Preserve form state for easy correction
- Allow users to retry requests
- Provide suggestions for common issues

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples and edge cases:

1. **Form Component Tests**
   - Render with all fields present
   - Accept valid inputs
   - Reject invalid inputs
   - Display validation errors
   - Submit with valid data

2. **Recommendation Card Tests**
   - Render with all required fields
   - Handle missing optional fields
   - Display correct data formatting
   - Apply correct styling

3. **API Integration Tests**
   - Health check request on mount
   - Recommendations request on form submit
   - Error handling for failed requests
   - Response parsing and data extraction

4. **State Management Tests**
   - Form state updates correctly
   - Loading state toggles appropriately
   - Error state displays and clears
   - API status updates correctly

### Property-Based Testing

Property-based tests will verify universal properties across many generated inputs:

1. **Form Validation Properties**
   - **Property 2**: Rating validation (0.0-5.0 range)
   - **Property 3**: Price validation (positive numbers)
   - **Property 4**: Limit validation (1-100 range)
   - **Property 5**: Invalid input prevention

2. **API Integration Properties**
   - **Property 6**: API request triggering
   - **Property 31**: Content-Type header correctness
   - **Property 32**: Response parsing correctness
   - **Property 33**: Error extraction correctness

3. **Display Properties**
   - **Property 12**: Card content completeness
   - **Property 25**: Filter tag display
   - **Property 30**: Pluralization correctness
   - **Property 37**: Recommendation details completeness

4. **State Management Properties**
   - **Property 19**: Loading state transitions
   - **Property 24**: Error message clearing
   - **Property 36**: Multiple submission handling

### Test Configuration

- Minimum 100 iterations per property test
- Each property test tagged with feature name and property number
- Tag format: `Feature: phase-6-react-migration, Property N: [property description]`
- Unit tests for specific examples and edge cases
- Property tests for universal correctness properties

### Testing Tools

- **Unit Testing**: Jest or Vitest
- **Property-Based Testing**: fast-check (JavaScript)
- **Component Testing**: React Testing Library
- **E2E Testing**: Playwright or Cypress

