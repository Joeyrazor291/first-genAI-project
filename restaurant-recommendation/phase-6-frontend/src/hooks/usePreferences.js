import { useState } from 'react'

/**
 * Custom hook for managing user preferences
 */
export function usePreferences() {
  const [preferences, setPreferences] = useState({
    cuisine: '',
    location: '',
    minRating: '',
    maxPrice: '',
    limit: 5
  })

  const updatePreference = (field, value) => {
    setPreferences(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const resetPreferences = () => {
    setPreferences({
      cuisine: '',
      location: '',
      minRating: '',
      maxPrice: '',
      limit: 5
    })
  }

  const buildPreferencesObject = () => {
    const prefs = {}
    
    if (preferences.cuisine?.trim()) prefs.cuisine = preferences.cuisine.trim()
    if (preferences.location?.trim()) prefs.location = preferences.location.trim()
    if (preferences.minRating) prefs.min_rating = parseFloat(preferences.minRating)
    if (preferences.maxPrice) prefs.max_price = parseFloat(preferences.maxPrice)
    if (preferences.limit) prefs.limit = parseInt(preferences.limit)
    
    return prefs
  }

  return {
    preferences,
    updatePreference,
    resetPreferences,
    buildPreferencesObject
  }
}
