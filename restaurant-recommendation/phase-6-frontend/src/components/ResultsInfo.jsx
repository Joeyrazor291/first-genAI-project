export function ResultsInfo({ totalFound, showing }) {
  return (
    <div className="text-gray-600 text-sm">
      <span className="font-semibold text-gray-900">
        Found {totalFound} restaurant{totalFound !== 1 ? 's' : ''}
      </span>
      <span className="ml-3">Showing {showing}</span>
    </div>
  )
}
