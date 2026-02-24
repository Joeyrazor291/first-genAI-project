# Quick Start - Phase 6 React Frontend

## 1-Minute Setup

### Prerequisites
- Node.js 16+ installed
- Phase 2 API running on `http://localhost:8000`

### Installation

```bash
cd restaurant-recommendation/phase-6-frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## What's New

This is the React 18+ version of Phase 6 frontend:
- ✅ React functional components with hooks
- ✅ Tailwind CSS styling
- ✅ Same features as vanilla JS version
- ✅ Better code organization
- ✅ Easier to maintain and extend

## File Structure

```
src/
├── components/     # 11 React components
├── hooks/          # 3 custom hooks
├── services/       # API communication
├── App.jsx         # Root component
└── index.css       # Tailwind CSS
```

## Available Scripts

```bash
npm run dev         # Start development server
npm run build       # Build for production
npm run preview     # Preview production build
npm test            # Run tests
npm run test:ui     # Run tests with UI
```

## Troubleshooting

### API Status Shows "Offline"
```bash
# Check if Phase 2 API is running
curl http://localhost:8000/health
```

### Port Already in Use
```bash
# Change port in vite.config.js
# Or kill process on port 5173
```

### Dependencies Not Installing
```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

1. **Verify Features**
   - Enter preferences and get recommendations
   - Check API status indicator
   - Test form validation
   - Try different filters

2. **Explore Code**
   - Check `src/components/` for UI components
   - Check `src/hooks/` for state management
   - Check `src/services/api.js` for API calls

3. **Customize**
   - Change API URL in `src/services/api.js`
   - Modify styling in `tailwind.config.js`
   - Add new components as needed

## Documentation

- `REACT_SETUP.md` - Detailed setup guide
- `MIGRATION_SUMMARY.md` - Complete migration details
- Component files have inline documentation

## Support

For issues:
1. Check browser console for errors
2. Verify Phase 2 API is running
3. Check `REACT_SETUP.md` for troubleshooting
4. Review component documentation

---

**Ready to go!** 🚀
