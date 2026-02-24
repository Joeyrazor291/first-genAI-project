import { useEffect, useRef } from 'react'

export function ErrorMessage({ message, isVisible }) {
  const errorRef = useRef(null)

  useEffect(() => {
    if (isVisible && errorRef.current) {
      errorRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    }
  }, [isVisible])

  if (!isVisible || !message) return null

  return (
    <div ref={errorRef} className="max-w-7xl mx-auto px-8 my-6">
      <div className="bg-red-50 border-l-4 border-red-500 text-red-900 p-4 rounded-lg whitespace-pre-line">
        <div className="flex items-start gap-3">
          <span className="text-xl">⚠️</span>
          <div>{message}</div>
        </div>
      </div>
    </div>
  )
}
