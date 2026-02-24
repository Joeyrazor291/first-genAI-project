import { useState, useEffect, useCallback } from 'react'
import { fetchHealthCheck } from '../services/api'

/**
 * Custom hook for managing API health status
 */
export function useAPIHealth() {
  const [apiStatus, setApiStatus] = useState('checking')

  const checkAPIHealth = useCallback(async () => {
    const result = await fetchHealthCheck()
    setApiStatus(result.status)
  }, [])

  useEffect(() => {
    checkAPIHealth()
  }, [checkAPIHealth])

  return {
    apiStatus,
    checkAPIHealth
  }
}
