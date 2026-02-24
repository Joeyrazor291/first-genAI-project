import { useState } from 'react'

/**
 * Custom hook for managing recommendations, loading, and error states
 */
export function useRecommendations() {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [resultsInfo, setResultsInfo] = useState(null)
  const [filtersApplied, setFiltersApplied] = useState(null)
  const [warnings, setWarnings] = useState([])

  const clearError = () => setError(null)
  const clearResults = () => {
    setRecommendations([])
    setResultsInfo(null)
    setFiltersApplied(null)
    setWarnings([])
  }

  return {
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
  }
}
