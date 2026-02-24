import { useEffect, useRef } from 'react'
import { FilterTags } from './FilterTags'
import { ResultsInfo } from './ResultsInfo'
import { RecommendationsList } from './RecommendationsList'

export function ResultsSection({ recommendations, resultsInfo, filtersApplied, warnings, isVisible }) {
  const resultsRef = useRef(null)

  useEffect(() => {
    if (isVisible && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, [isVisible])

  if (!isVisible || !recommendations || recommendations.length === 0) {
    return null
  }

  return (
    <section ref={resultsRef} className="w-full">
      {/* Results Header */}
      <div className="bg-white border-b border-gray-200 px-8 py-4 mb-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {resultsInfo?.count} restaurants found
              </h2>
              <p className="text-sm text-gray-600">Delivering to Whitefield, Bengaluru</p>
            </div>
            <button className="text-red-500 font-semibold text-sm hover:text-red-600">
              ✎ Edit Preferences
            </button>
          </div>

          {/* Filter Chips */}
          <div className="flex flex-wrap gap-2 items-center">
            <button className="px-4 py-2 border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-gray-400">
              ☰ Filters
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-gray-400">
              3.5+ ⭐
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-gray-400">
              4+ ⭐
            </button>
            <button className="px-4 py-2 bg-red-500 text-white rounded-full text-sm font-medium hover:bg-red-600">
              4.5+ ⭐
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-gray-400">
              Cuisine (2) ▼
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-gray-400">
              Price ▼
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-gray-400">
              Most Relevant ▼
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-gray-400">
              ✕ Clear
            </button>
          </div>
        </div>
      </div>

      {/* Recommendations Grid */}
      <div className="max-w-7xl mx-auto px-8">
        <RecommendationsList recommendations={recommendations} />
      </div>
    </section>
  )
}
