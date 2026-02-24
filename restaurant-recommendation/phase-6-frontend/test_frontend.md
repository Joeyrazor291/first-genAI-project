# Frontend Testing Guide

## Quick Start Testing

### Step 1: Start the Backend API

Open a terminal and run:

```bash
cd restaurant-recommendation/phase-2-recommendation-api
python src/main.py
```

The API should start on `http://localhost:8000`

### Step 2: Start the Frontend Server

Open another terminal and run:

```bash
cd restaurant-recommendation/phase-6-frontend
python serve.py
```

The frontend should start on `http://localhost:8080`

### Step 3: Open in Browser

Navigate to: `http://localhost:8080`

## Manual Test Cases

### Test 1: API Status Check
**Expected**: Status indicator shows "Online" (green)
**If Offline**: Check that Phase 2 API is running

### Test 2: Basic Recommendation Request
1. Leave all fields empty except "Number of Results"
2. Set "Number of Results" to 5
3. Click "Get Recommendations"

**Expected**:
- Loading spinner appears
- Results display with 5 restaurants
- Each card shows: name, cuisine, location, rating, price, explanation

### Test 3: Filtered Request
1. Enter "Italian" in Cuisine Type
2. Enter "4.0" in Minimum Rating
3. Set "Number of Results" to 3
4. Click "Get Recommendations"

**Expected**:
- Filter tags show "Cuisine: Italian" and "Min Rating: 4.0"
- Results show Italian restaurants with rating >= 4.0
- Maximum 3 results displayed

### Test 4: Invalid Input
1. Enter "10" in Minimum Rating (invalid, max is 5)
2. Click "Get Recommendations"

**Expected**:
- Error message: "Rating must be between 0 and 5"
- No API call made

### Test 5: No Results
1. Enter "5.0" in Minimum Rating
2. Enter "1" in Maximum Price
3. Click "Get Recommendations"

**Expected**:
- Error message: "No restaurants found matching your preferences..."

### Test 6: Responsive Design
1. Resize browser window to mobile size (< 768px)

**Expected**:
- Form fields stack vertically
- Cards display in single column
- All elements remain readable and functional

### Test 7: API Offline Handling
1. Stop the Phase 2 API server
2. Try to get recommendations

**Expected**:
- Error message about API unavailability
- Status indicator shows "Offline"

## Visual Checks

### Layout
- [ ] Header displays with gradient background
- [ ] Form is centered and readable
- [ ] Cards have consistent spacing
- [ ] Footer is at bottom

### Interactions
- [ ] Input fields highlight on focus (blue border)
- [ ] Submit button changes color on hover
- [ ] Cards elevate on hover
- [ ] Smooth scroll to results

### Content
- [ ] Restaurant names display correctly
- [ ] Ratings show with stars
- [ ] Prices formatted as currency
- [ ] AI explanations are readable
- [ ] Addresses display when available

### Responsive
- [ ] Mobile view (< 768px): Single column layout
- [ ] Tablet view (768px - 1024px): 2 column cards
- [ ] Desktop view (> 1024px): 3 column cards

## Browser Testing

Test in multiple browsers:
- [ ] Chrome
- [ ] Firefox
- [ ] Safari (Mac)
- [ ] Edge

## Performance Checks

- [ ] Page loads in < 1 second
- [ ] API health check completes quickly
- [ ] Recommendations load in 1-3 seconds
- [ ] No console errors
- [ ] No network errors

## Troubleshooting

### Issue: API Status shows "Offline"
**Solution**: 
1. Check Phase 2 API is running: `curl http://localhost:8000/health`
2. Verify port 8000 is not blocked
3. Check API logs for errors

### Issue: CORS Errors
**Solution**:
1. Ensure Phase 2 API has CORS middleware enabled
2. Don't use `file://` protocol - use HTTP server
3. Check browser console for specific CORS error

### Issue: No Recommendations Display
**Solution**:
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify API response in Network tab
4. Check if Phase 1 database exists

### Issue: Styling Looks Broken
**Solution**:
1. Verify `styles.css` is loaded (check Network tab)
2. Clear browser cache
3. Check for CSS syntax errors

## Success Criteria

All tests pass when:
- ✅ API status indicator works
- ✅ Form validation works
- ✅ Recommendations display correctly
- ✅ Error handling works
- ✅ Responsive design works
- ✅ All interactions are smooth
- ✅ No console errors
- ✅ Works in all major browsers

## Next Steps After Testing

If all tests pass:
1. Document any issues found
2. Take screenshots for documentation
3. Prepare for end-to-end demo
4. Consider deployment options

If tests fail:
1. Note specific failure
2. Check relevant logs
3. Verify all phases are running
4. Review configuration
