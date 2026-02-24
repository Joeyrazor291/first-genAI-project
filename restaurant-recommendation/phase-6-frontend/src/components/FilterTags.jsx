export function FilterTags({ filtersApplied, warnings }) {
  if (!filtersApplied || Object.keys(filtersApplied).length === 0) {
    return null
  }

  return (
    <div className="bg-blue-100 px-4 py-3 rounded-lg mb-6 text-sm text-blue-900">
      <div className="font-semibold mb-2 text-blue-900">Active Filters:</div>
      <div>
        {Object.entries(filtersApplied).map(([key, value]) => {
          const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
          return (
            <span key={key} className="filter-tag">
              {label}: {value}
            </span>
          )
        })}
      </div>
      {warnings && warnings.length > 0 && (
        <div className="mt-3">
          {warnings.map((warning, idx) => (
            <div key={idx} className="mt-2 p-2.5 bg-yellow-100 border-l-4 border-yellow-500 rounded text-yellow-900 text-xs">
              ⚠️ {warning}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
