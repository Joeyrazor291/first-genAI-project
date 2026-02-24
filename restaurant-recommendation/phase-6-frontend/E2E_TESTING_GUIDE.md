# Phase 6 React Frontend - End-to-End Testing Guide

## Overview

This guide covers end-to-end testing for the React frontend migration. Tests verify that all features work correctly and maintain feature parity with the original vanilla JavaScript version.

## Test Scope

### Frontend Features to Test

1. **Form Functionality**
   - ✅ All 5 input fields accept values
   - ✅ Form validation works correctly
   - ✅ Error messages display for invalid inputs
   - ✅ Form submission triggers API request

2. **API Integration**
   - ✅ Health check on app load
   - ✅ API status indicator updates
   - ✅ Recommendations request sent with correct data
   - ✅ Error responses handled gracefully

3. **UI Components**
   - ✅ Header displays correctly
   - ✅ Form renders all fields
   - ✅ Loading state appears during request
   - ✅ Error messages display and auto-scroll
   - ✅ Recommendation cards display all data
   - ✅ Filter tags show active filters
   - ✅ Results info shows correct counts
   - ✅ Footer displays API status

4. **User Interactions**
   - ✅ Form input changes update state
   - ✅ Submit button triggers submission
   - ✅ Button disabled during loading
   - ✅ Cards have hover effects
   - ✅ Error messages auto-scroll into view

5. **Responsive Design**
   - ✅ Mobile layout (< 768px)
   - ✅ Tablet layout (768px - 1024px)
   - ✅ Desktop layout (> 1024px)

6. **Animations**
   - ✅ Spinner rotates smoothly
   - ✅ Cards fade in with stagger
   - ✅ Hover effects smooth
   - ✅ Transitions smooth

## Manual Testing Checklist

### Pre-Test Setup

```bash
# 1. Start Phase 2 API
cd ../phase-2-recommendation-api
python -m uvicorn src.main:app --reload

# 2. Start React frontend (in new terminal)
cd ../phase-6-frontend
npm install
npm run dev

# 3. Open browser to http://localhost:5173
```

### Test Cases

#### Test 1: Application Load
- [ ] Page loads without errors
- [ ] Header displays with title and subtitle
- [ ] Form displays with all 5 input fields
- [ ] API status shows "Online" or "Offline"
- [ ] Footer displays with API status

#### Test 2: Form Validation
- [ ] Enter rating = 6 → Error: "Rating must be between 0 and 5"
- [ ] Enter price = -10 → Error: "Price must be positive"
- [ ] Enter limit = 0 → Error: "Limit must be between 1 and 100"
- [ ] Enter limit = 101 → Error: "Limit must be between 1 and 100"
- [ ] Valid inputs → No error message

#### Test 3: Successful Recommendation Flow
- [ ] Enter cuisine: "Italian"
- [ ] Enter location: "Downtown"
- [ ] Enter min rating: "3.5"
- [ ] Enter max price: "50"
- [ ] Enter limit: "5"
- [ ] Click "Get Recommendations"
- [ ] Loading spinner appears
- [ ] Button shows "Loading..." with spinner
- [ ] Recommendations display after API response
- [ ] Filter tags show active filters
- [ ] Results info shows count
- [ ] Each card shows: name, cuisine, location, rating, price, explanation

#### Test 4: No Results Scenario
- [ ] Enter impossible criteria (e.g., rating = 5.0, max_price = 1)
- [ ] Click "Get Recommendations"
- [ ] Error message displays with suggestions
- [ ] Message suggests adjusting filters

#### Test 5: API Error Handling
- [ ] Stop Phase 2 API
- [ ] Try to get recommendations
- [ ] Error message displays
- [ ] Restart API
- [ ] Try again → Works correctly

#### Test 6: Multiple Submissions
- [ ] Submit form with cuisine "Italian"
- [ ] Get recommendations
- [ ] Change cuisine to "Chinese"
- [ ] Submit again
- [ ] New recommendations display
- [ ] Previous results cleared
- [ ] No state corruption

#### Test 7: Responsive Design - Mobile
- [ ] Open DevTools (F12)
- [ ] Set viewport to 375x667 (iPhone)
- [ ] Form fields stack vertically
- [ ] Recommendation cards single column
- [ ] All text readable
- [ ] Buttons clickable

#### Test 8: Responsive Design - Tablet
- [ ] Set viewport to 768x1024 (iPad)
- [ ] Form fields in 2-3 columns
- [ ] Recommendation cards 2 columns
- [ ] Layout adapts properly

#### Test 9: Responsive Design - Desktop
- [ ] Set viewport to 1920x1080
- [ ] Form fields in 5 columns
- [ ] Recommendation cards 3 columns
- [ ] Full layout displays

#### Test 10: Animations
- [ ] Get recommendations
- [ ] Cards fade in with stagger effect
- [ ] Hover over card → Elevation effect
- [ ] Spinner rotates smoothly
- [ ] Error message scrolls smoothly into view

#### Test 11: Filter Tags
- [ ] Submit with cuisine and location
- [ ] Filter tags display both filters
- [ ] Submit with no filters
- [ ] Filter tags section hidden
- [ ] Submit with only cuisine
- [ ] Only cuisine tag displays

#### Test 12: Results Information
- [ ] Get recommendations
- [ ] Results info shows "Found X restaurants"
- [ ] Results info shows "Showing Y"
- [ ] For 1 restaurant: "Found 1 restaurant"
- [ ] For 5 restaurants: "Found 5 restaurants"

#### Test 13: Recommendation Card Details
- [ ] Each card shows rank (#1, #2, etc.)
- [ ] Restaurant name displays
- [ ] Cuisine displays with 🍽️ icon
- [ ] Location displays with 📍 icon
- [ ] Rating displays with stars
- [ ] Price displays in rupees (₹)
- [ ] Explanation displays in highlighted box
- [ ] Address displays if available

#### Test 14: API Health Check
- [ ] API running → Status shows "Online" (green)
- [ ] API stopped → Status shows "Offline" (red)
- [ ] API degraded → Status shows "Degraded" (yellow)

#### Test 15: Form State Persistence
- [ ] Enter cuisine "Italian"
- [ ] Enter location "Downtown"
- [ ] Don't submit
- [ ] Refresh page
- [ ] Form fields cleared (expected behavior)
- [ ] Enter values again
- [ ] Submit works correctly

## Automated Testing (Optional)

### Using Playwright for E2E Tests

```bash
# Install Playwright
npm install -D @playwright/test

# Create test file
cat > tests/e2e.spec.js << 'EOF'
import { test, expect } from '@playwright/test';

test('complete recommendation flow', async ({ page }) => {
  // Navigate to app
  await page.goto('http://localhost:5173');
  
  // Check header
  await expect(page.locator('h1')).toContainText('AI Restaurant Recommendations');
  
  // Fill form
  await page.fill('input[name="cuisine"]', 'Italian');
  await page.fill('input[name="location"]', 'Downtown');
  await page.fill('input[name="minRating"]', '3.5');
  await page.fill('input[name="maxPrice"]', '50');
  
  // Submit
  await page.click('button[type="submit"]');
  
  // Wait for results
  await page.waitForSelector('.card');
  
  // Verify results
  const cards = await page.locator('.card').count();
  expect(cards).toBeGreaterThan(0);
});
EOF

# Run tests
npx playwright test
```

### Using Vitest for Component Tests

```bash
# Run component tests
npm test

# Run with coverage
npm test -- --coverage
```

## Performance Testing

### Load Testing

```bash
# Test with multiple rapid requests
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/v1/recommendations \
    -H "Content-Type: application/json" \
    -d '{"cuisine":"Italian","limit":5}' &
done
wait
```

### Response Time Benchmarks

- Form submission: < 100ms
- API request: < 2s
- Recommendation display: < 500ms
- Total flow: < 3s

## Browser Compatibility Testing

### Browsers to Test

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari

### Test on Each Browser

1. Load application
2. Submit form with valid data
3. Verify recommendations display
4. Check responsive design
5. Verify animations work

## Accessibility Testing

### Keyboard Navigation

- [ ] Tab through form fields
- [ ] Tab to submit button
- [ ] Enter key submits form
- [ ] Tab through recommendation cards

### Screen Reader Testing

- [ ] Form labels readable
- [ ] Error messages announced
- [ ] Results announced
- [ ] Button states announced

## Common Issues & Solutions

### Issue: API Status Shows "Offline"
**Solution:**
1. Verify Phase 2 API is running
2. Check API URL in `src/services/api.js`
3. Check browser console for CORS errors

### Issue: Form Submission Fails
**Solution:**
1. Check browser console for errors
2. Verify API is running
3. Check network tab in DevTools
4. Verify request format

### Issue: Recommendations Don't Display
**Solution:**
1. Check API response in network tab
2. Verify database has data
3. Check browser console for errors
4. Try with broader filters

### Issue: Responsive Design Broken
**Solution:**
1. Clear browser cache
2. Hard refresh (Ctrl+Shift+R)
3. Check Tailwind CSS is loaded
4. Verify viewport meta tag

## Test Results Template

```
Test Date: _______________
Tester: ___________________
Browser: __________________
OS: _______________________

Test Results:
- Application Load: ✅ / ❌
- Form Validation: ✅ / ❌
- Successful Flow: ✅ / ❌
- No Results: ✅ / ❌
- API Error Handling: ✅ / ❌
- Multiple Submissions: ✅ / ❌
- Mobile Responsive: ✅ / ❌
- Tablet Responsive: ✅ / ❌
- Desktop Responsive: ✅ / ❌
- Animations: ✅ / ❌
- Filter Tags: ✅ / ❌
- Results Info: ✅ / ❌
- Card Details: ✅ / ❌
- API Health Check: ✅ / ❌
- Form State: ✅ / ❌

Issues Found:
1. ___________________________
2. ___________________________
3. ___________________________

Overall Status: ✅ PASS / ❌ FAIL
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
        working-directory: restaurant-recommendation/phase-6-frontend
      
      - name: Run tests
        run: npm test
        working-directory: restaurant-recommendation/phase-6-frontend
```

## Sign-Off

When all tests pass:

```
✅ All manual tests completed
✅ All automated tests passing
✅ No console errors
✅ Responsive design verified
✅ Animations working
✅ API integration verified
✅ Ready for production

Tested by: ___________________
Date: _______________________
```

---

## Support

For testing issues:
1. Check browser console (F12)
2. Check network tab for API calls
3. Verify Phase 2 API is running
4. Review `REACT_SETUP.md` for setup
5. Check `MIGRATION_SUMMARY.md` for details

---

**Happy Testing!** 🧪
