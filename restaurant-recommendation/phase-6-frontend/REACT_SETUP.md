# Phase 6 React Frontend - Setup Guide

This is the React 18+ version of the Phase 6 frontend, migrated from vanilla JavaScript.

## Prerequisites

- Node.js 16+ and npm/yarn
- Phase 2 API running on `http://localhost:8000`
- Phase 1 Database at `../phase-1-data-pipeline/data/restaurant.db`

## Installation

1. Navigate to the frontend directory:
```bash
cd restaurant-recommendation/phase-6-frontend
```

2. Install dependencies:
```bash
npm install
```

## Development

Start the development server:
```bash
npm run dev
```

The application will open at `http://localhost:5173`

## Building for Production

Create an optimized production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Testing

Run tests:
```bash
npm test
```

Run tests with UI:
```bash
npm run test:ui
```

## Project Structure

```
src/
├── components/          # React components
│   ├── Header.jsx
│   ├── PreferenceForm.jsx
│   ├── LoadingState.jsx
│   ├── ErrorMessage.jsx
│   ├── APIHealthCheck.jsx
│   ├── Footer.jsx
│   ├── RecommendationCard.jsx
│   ├── FilterTags.jsx
│   ├── ResultsInfo.jsx
│   ├── RecommendationsList.jsx
│   └── ResultsSection.jsx
├── hooks/               # Custom React hooks
│   ├── usePreferences.js
│   ├── useRecommendations.js
│   └── useAPIHealth.js
├── services/            # API communication
│   └── api.js
├── App.jsx              # Root component
├── main.jsx             # Entry point
└── index.css            # Tailwind CSS
```

## Configuration

### API Base URL

To change the API endpoint, edit `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000'  // Change this
```

## Features

- ✅ Preference form with validation
- ✅ Real-time API health check
- ✅ Recommendation cards with details
- ✅ Loading states and error handling
- ✅ Responsive design (mobile-friendly)
- ✅ Filter tags display
- ✅ Smooth animations and transitions
- ✅ Tailwind CSS styling

## Troubleshooting

### API Status Shows "Offline"

1. Verify Phase 2 API is running:
```bash
curl http://localhost:8000/health
```

2. Check if the API port matches `src/services/api.js`

3. Ensure CORS is enabled in the API

### No Recommendations Found

1. Try broader filters (remove some constraints)
2. Check if Phase 1 database has data
3. Verify Phase 5 engine is initialized

## Migration Notes

This React version maintains 100% feature parity with the original vanilla JavaScript implementation:

- All UI logic converted to React functional components with hooks
- All styling converted from CSS to Tailwind CSS utility classes
- API integration preserved exactly as-is
- Visual appearance and behavior identical to original
- Responsive design maintained
- All animations and transitions preserved

## License

Part of the AI Restaurant Recommendation Service project.
