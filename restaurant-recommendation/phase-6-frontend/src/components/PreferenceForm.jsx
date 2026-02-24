import { useCallback, useState } from 'react'

const POPULAR_LOCATIONS = ['Koramangala', 'Indiranagar', 'Whitefield', 'HSR Layout', 'MG Road', 'Jayanagar', 'Marathahalli', 'Electronic City', 'BTM Layout', 'Hebbal']

const CUISINE_OPTIONS = [
  { name: 'North Indian', emoji: '🍛' },
  { name: 'South Indian', emoji: '🥘' },
  { name: 'Chinese', emoji: '🥢' },
  { name: 'Italian', emoji: '🍝' },
  { name: 'Continental', emoji: '🍽️' },
  { name: 'Mughlai', emoji: '🍖' },
  { name: 'Biryani', emoji: '🍚' },
  { name: 'Street Food', emoji: '🌮' },
  { name: 'Desserts', emoji: '🍰' },
  { name: 'Cafe', emoji: '☕' }
]

const PRICE_RANGES = [
  { label: 'Budget-friendly', range: 'Under ₹300', value: 300 },
  { label: 'Moderate', range: '₹300-600', value: 600 },
  { label: 'Premium', range: '₹600-1200', value: 1200 },
  { label: 'Fine Dining', range: '₹1200+', value: 2000 }
]

const RATING_OPTIONS = [
  { label: '3.5+', value: 3.5 },
  { label: '4+', value: 4.0 },
  { label: '4.5+', value: 4.5 },
  { label: '5+', value: 5.0 }
]

const SORT_OPTIONS = [
  { label: 'Most Relevant', value: 'relevant' },
  { label: 'Highest Rated', value: 'rating' },
  { label: 'Fastest Delivery', value: 'delivery' },
  { label: 'Price: Low to High', value: 'price_asc' },
  { label: 'Price: High to Low', value: 'price_desc' }
]

const RECOMMENDATION_COUNT_OPTIONS = [
  { label: '5', value: 5 },
  { label: '10', value: 10 },
  { label: '15', value: 15 },
  { label: '20', value: 20 },
  { label: '25', value: 25 },
  { label: '30', value: 30 }
]

export function PreferenceForm({ preferences, onInputChange, onSubmit, isLoading }) {
  const [selectedCuisines, setSelectedCuisines] = useState([])
  const [priceRange, setPriceRange] = useState(2000)
  const [selectedRating, setSelectedRating] = useState(null)
  const [selectedSort, setSelectedSort] = useState('relevant')
  const [selectedCount, setSelectedCount] = useState(10)

  const handleSubmit = useCallback((e) => {
    e.preventDefault()
    onSubmit()
  }, [onSubmit])

  const toggleCuisine = (cuisineName) => {
    setSelectedCuisines(prev => {
      const newCuisines = prev.includes(cuisineName)
        ? prev.filter(c => c !== cuisineName)
        : [...prev, cuisineName]
      
      // Update the preference with selected cuisines
      onInputChange('cuisine', newCuisines.join(', '))
      return newCuisines
    })
  }

  const handleRatingSelect = (value) => {
    setSelectedRating(value)
    onInputChange('minRating', value)
  }

  const handlePriceChange = (value) => {
    setPriceRange(value)
    onInputChange('maxPrice', value)
  }

  const handleCountSelect = (value) => {
    setSelectedCount(value)
    onInputChange('limit', value)
  }

  return (
    <section className="w-full">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Location Section */}
        <div>
          <label className="flex items-center gap-2 text-gray-900 font-semibold mb-3">
            <span className="text-red-500">📍</span>
            Location in Bengaluru
          </label>
          <input
            type="text"
            placeholder="Enter locality (e.g., Koramangala, Indiranagar)"
            value={preferences.location}
            onChange={(e) => onInputChange('location', e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500 focus:ring-1 focus:ring-red-200 text-gray-900"
          />
          <div className="mt-3 flex flex-wrap gap-2">
            {POPULAR_LOCATIONS.map(loc => (
              <button
                key={loc}
                type="button"
                onClick={() => onInputChange('location', loc)}
                className={`px-3 py-1.5 rounded-full text-sm font-medium transition-all ${
                  preferences.location === loc
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {loc}
              </button>
            ))}
          </div>
        </div>

        {/* Cuisines Section */}
        <div>
          <label className="flex items-center gap-2 text-gray-900 font-semibold mb-3">
            <span className="text-red-500">🍽️</span>
            Cuisines {selectedCuisines.length > 0 && `(${selectedCuisines.length} selected)`}
          </label>
          
          {selectedCuisines.length > 0 && (
            <div className="mb-3 flex flex-wrap gap-2">
              {selectedCuisines.map(cuisine => (
                <div
                  key={cuisine}
                  className="inline-flex items-center gap-2 bg-red-500 text-white px-3 py-1.5 rounded-full text-sm font-medium"
                >
                  <span>✕</span>
                  {cuisine}
                </div>
              ))}
            </div>
          )}

          <input
            type="text"
            placeholder="Type to search cuisines..."
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500 focus:ring-1 focus:ring-red-200 text-gray-900 mb-4"
          />

          <div className="grid grid-cols-5 gap-3">
            {CUISINE_OPTIONS.map(cuisine => (
              <button
                key={cuisine.name}
                type="button"
                onClick={() => toggleCuisine(cuisine.name)}
                className={`p-4 rounded-lg border-2 transition-all text-center ${
                  selectedCuisines.includes(cuisine.name)
                    ? 'border-red-500 bg-red-50'
                    : 'border-gray-200 bg-white hover:border-gray-300'
                }`}
              >
                <div className="text-3xl mb-2">{cuisine.emoji}</div>
                <div className="text-sm font-medium text-gray-900">{cuisine.name}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Price Range Section */}
        <div>
          <label className="flex items-center gap-2 text-gray-900 font-semibold mb-3">
            <span className="text-red-500">💵</span>
            Price Range (for two people)
          </label>
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>₹0</span>
            <span>₹{priceRange}</span>
          </div>
          <input
            type="range"
            min="0"
            max="2000"
            value={priceRange}
            onChange={(e) => handlePriceChange(e.target.value)}
            className="w-full h-2 bg-red-500 rounded-lg appearance-none cursor-pointer accent-red-500"
          />
          <div className="grid grid-cols-4 gap-3 mt-4">
            {PRICE_RANGES.map(price => (
              <button
                key={price.value}
                type="button"
                onClick={() => handlePriceChange(price.value)}
                className={`p-3 rounded-lg border-2 text-center transition-all ${
                  parseInt(priceRange) === price.value
                    ? 'border-red-500 bg-red-50'
                    : 'border-gray-200 bg-white hover:border-gray-300'
                }`}
              >
                <div className="text-red-500 font-bold text-lg">{price.label.split('-')[0]}</div>
                <div className="text-xs text-gray-600">{price.range}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Rating Section */}
        <div>
          <label className="flex items-center gap-2 text-gray-900 font-semibold mb-3">
            <span className="text-red-500">⭐</span>
            Minimum Rating
          </label>
          <div className="grid grid-cols-4 gap-3">
            {RATING_OPTIONS.map(rating => (
              <button
                key={rating.value}
                type="button"
                onClick={() => handleRatingSelect(rating.value)}
                className={`p-3 rounded-lg border-2 text-center transition-all font-medium ${
                  selectedRating === rating.value
                    ? 'border-gray-900 bg-white'
                    : 'border-gray-200 bg-white hover:border-gray-300'
                }`}
              >
                <span className="text-gray-400">⭐</span> {rating.label}
              </button>
            ))}
          </div>
        </div>

        {/* Number of Recommendations Section */}
        <div>
          <label className="flex items-center gap-2 text-gray-900 font-semibold mb-3">
            <span className="text-red-500">🔢</span>
            Number of Recommendations
          </label>
          <div className="grid grid-cols-6 gap-3">
            {RECOMMENDATION_COUNT_OPTIONS.map(option => (
              <button
                key={option.value}
                type="button"
                onClick={() => handleCountSelect(option.value)}
                className={`p-3 rounded-lg border-2 text-center transition-all font-medium ${
                  selectedCount === option.value
                    ? 'border-red-500 bg-red-50 text-gray-900'
                    : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        {/* Sort Section */}
        <div>
          <label className="text-gray-900 font-semibold mb-3 block">Sort Results By</label>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {SORT_OPTIONS.map(sort => (
              <button
                key={sort.value}
                type="button"
                onClick={() => setSelectedSort(sort.value)}
                className={`p-3 rounded-lg border-2 text-center transition-all font-medium text-sm ${
                  selectedSort === sort.value
                    ? 'border-red-500 bg-red-50 text-gray-900'
                    : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                }`}
              >
                {sort.label}
              </button>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-red-500 hover:bg-red-600 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition-all duration-300 flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <span className="spinner-small"></span>
              Finding Restaurants...
            </>
          ) : (
            <>
              Find Restaurants <span>→</span>
            </>
          )}
        </button>

        <p className="text-center text-sm text-gray-600">You can always adjust these preferences later</p>
      </form>
    </section>
  )
}
