/**
 * API Service Layer
 * Handles all communication with the Phase 2 recommendation API
 */

const API_BASE_URL = 'http://localhost:8000'
const API_VERSION = 'v1'

/**
 * Check API health status
 * @returns {Promise<Object>} Health check response
 */
export async function fetchHealthCheck() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`)
    const data = await response.json()
    
    if (response.ok && data.status === 'healthy') {
      return { status: 'online', data }
    } else if (data.status === 'degraded') {
      return { status: 'degraded', data }
    } else {
      return { status: 'offline', data }
    }
  } catch (error) {
    return { status: 'offline', error: error.message }
  }
}

/**
 * Fetch recommendations from API
 * @param {Object} preferences - User preferences
 * @returns {Promise<Object>} Recommendations response
 */
export async function fetchRecommendations(preferences) {
  const url = `${API_BASE_URL}/api/${API_VERSION}/recommendations`
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(preferences)
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      const errorMsg = data.detail?.error || data.detail || 'Failed to fetch recommendations'
      throw new Error(errorMsg)
    }
    
    return data
  } catch (error) {
    throw error
  }
}

export { API_BASE_URL, API_VERSION }
