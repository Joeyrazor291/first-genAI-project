export function RecommendationCard({ restaurant, explanation, rank }) {
  // Handle both old and new API response formats
  const name = restaurant.name || restaurant.restaurant_name || 'Unknown Restaurant'
  const cuisine = restaurant.cuisine || restaurant.cuisines || 'Various'
  const location = restaurant.location || restaurant.locality || restaurant.city || 'Unknown'
  const ratingValue = restaurant.rating || restaurant.aggregate_rating
  const rating = ratingValue ? parseFloat(ratingValue).toFixed(1) : 'N/A'
  const priceValue = restaurant.price || restaurant.average_cost_for_two
  const price = priceValue ? `₹${parseFloat(priceValue).toFixed(0)}` : 'N/A'
  const address = restaurant.address

  return (
    <div className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow border border-gray-200">
      {/* Image Placeholder */}
      <div className="relative bg-gradient-to-br from-gray-300 to-gray-400 h-48 flex items-center justify-center overflow-hidden">
        <div className="text-6xl opacity-30">🍽️</div>
        <div className="absolute top-3 right-3 bg-white rounded-full p-2 cursor-pointer hover:bg-gray-100">
          <span className="text-lg">♡</span>
        </div>
        <div className="absolute bottom-3 left-3 bg-black bg-opacity-60 text-white px-3 py-1 rounded text-sm font-medium">
          50% off on orders above ₹300
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Restaurant Name and Rating */}
        <div className="flex items-start justify-between mb-2">
          <h3 className="text-lg font-bold text-gray-900 flex-1">{name}</h3>
          <div className="bg-green-600 text-white px-2 py-1 rounded text-sm font-bold ml-2">
            ⭐ {rating}
          </div>
        </div>

        {/* Cuisine and Location */}
        <p className="text-sm text-gray-600 mb-3">
          {cuisine} • {location}
        </p>

        {/* Details Row */}
        <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
          <span>⏱️ 25-30 min</span>
          <span>🚚 2.1 km</span>
          <span className="text-red-500 font-semibold">{price}</span>
        </div>

        {/* AI Explanation */}
        {explanation && (
          <div className="bg-blue-50 border-l-4 border-blue-500 p-3 rounded text-sm text-gray-700 mb-3">
            <p className="m-0">{explanation}</p>
          </div>
        )}

        {/* Address */}
        {address && (
          <p className="text-xs text-gray-500 mt-3 pt-3 border-t border-gray-200">
            {address}
          </p>
        )}
      </div>
    </div>
  )
}
