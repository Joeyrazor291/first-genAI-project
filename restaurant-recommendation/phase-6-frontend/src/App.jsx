import { useCallback } from 'react'
import { Header } from './components/Header'
import { PreferenceForm } from './components/PreferenceForm'
import { LoadingState } from './components/LoadingState'
import { ErrorMessage } from './components/ErrorMessage'
import { ResultsSection } from './components/ResultsSection'
import { Footer } from './components/Footer'
import { usePreferences } from './hooks/usePreferences'
import { useRecommendations } from './hooks/useRecommendations'
import { useAPIHealth } from './hooks/useAPIHealth'
import { fetchRecommendations } from './services/api'

function App() {
  const { preferences, updatePreference, buildPreferencesObject } = usePreferences()
  const {
    recommendations,
    setRecommendations,
    loading,
    setLoading,
    error,
    setError,
    clearError,
    resultsInfo,
    setResultsInfo,
    filtersApplied,
    setFiltersApplied,
    warnings,
    setWarnings,
    clearResults
  } = useRecommendations()
  const { apiStatus } = useAPIHealth()

  const validatePreferences = useCallback((prefs) => {
    if (prefs.min_rating !== undefined) {
      if (prefs.min_rating < 0 || prefs.min_rating > 5) {
        return { valid: false, message: 'Rating must be between 0 and 5' }
      }
    }

    if (prefs.max_price !== undefined) {
      if (prefs.max_price < 0) {
        return { valid: false, message: 'Price must be positive' }
      }
    }

    if (prefs.limit !== undefined) {
      if (prefs.limit < 1 || prefs.limit > 100) {
        return { valid: false, message: 'Limit must be between 1 and 100' }
      }
    }

    return { valid: true }
  }, [])

  const handleFormSubmit = useCallback(async () => {
    clearError()
    clearResults()

    const prefs = buildPreferencesObject()
    const validation = validatePreferences(prefs)

    if (!validation.valid) {
      setError(validation.message)
      return
    }

    setLoading(true)

    try {
      const data = await fetchRecommendations(prefs)
      const { success, count, total_found, recommendations: recs, filters_applied, warnings: warns } = data

      if (!success || count === 0) {
        let errorMsg = 'No restaurants found matching your preferences. '

        if (filters_applied) {
          errorMsg += 'Try:\n'
          if (filters_applied.location) {
            errorMsg += '• Using a different location (e.g., "downtown", "uptown", "midtown")\n'
          }
          if (filters_applied.max_price) {
            errorMsg += '• Increasing your maximum price\n'
          }
          if (filters_applied.min_rating) {
            errorMsg += '• Lowering your minimum rating\n'
          }
          if (filters_applied.cuisine) {
            errorMsg += '• Trying a different cuisine\n'
          }
          errorMsg += '\nOr visit the Debug Page to see all available options.'
        }

        setError(errorMsg)
      } else {
        setRecommendations(recs)
        setResultsInfo({ count, total_found })
        setFiltersApplied(filters_applied)
        setWarnings(warns || [])
      }
    } catch (err) {
      setError(err.message || 'Failed to fetch recommendations')
    } finally {
      setLoading(false)
    }
  }, [buildPreferencesObject, validatePreferences, clearError, clearResults, setLoading, setError, setRecommendations, setResultsInfo, setFiltersApplied, setWarnings])

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Hero Section */}
      <div className="bg-white border-b border-gray-200 py-12 px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-2">Find Your Perfect Meal</h2>
          <p className="text-gray-600">Tell us your preferences and we'll show you the best restaurants</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-8 py-8">
        <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
          <PreferenceForm
            preferences={preferences}
            onInputChange={updatePreference}
            onSubmit={handleFormSubmit}
            isLoading={loading}
          />
        </div>

        <ErrorMessage message={error} isVisible={!!error} />
        <LoadingState isVisible={loading} />
        
        {recommendations.length > 0 && (
          <div>
            <ResultsSection
              recommendations={recommendations}
              resultsInfo={resultsInfo}
              filtersApplied={filtersApplied}
              warnings={warnings}
              isVisible={recommendations.length > 0}
            />
          </div>
        )}
      </div>

      <Footer apiStatus={apiStatus} />
    </div>
  )
}

export default App
