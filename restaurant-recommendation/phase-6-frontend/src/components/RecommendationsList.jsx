import { RecommendationCard } from './RecommendationCard'

export function RecommendationsList({ recommendations }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {recommendations.map((rec, index) => {
        // Create a unique key using restaurant name + location to prevent duplicate rendering
        const uniqueKey = `${(rec.restaurant?.name || rec.name || '').toLowerCase()}-${(rec.restaurant?.location || rec.location || '').toLowerCase()}-${index}`
        
        return (
          <div key={uniqueKey} className="animate-fadeIn" style={{ animationDelay: `${index * 0.1}s` }}>
            <RecommendationCard
              restaurant={rec.restaurant || rec}
              explanation={rec.explanation || 'Great choice based on your preferences!'}
              rank={index + 1}
            />
          </div>
        )
      })}
    </div>
  )
}
