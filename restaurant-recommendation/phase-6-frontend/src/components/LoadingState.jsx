export function LoadingState({ isVisible }) {
  if (!isVisible) return null

  return (
    <div className="max-w-7xl mx-auto px-8 py-16">
      <div className="bg-white rounded-lg p-12 text-center">
        <div className="spinner-large mb-6"></div>
        <p className="text-lg text-gray-700 font-medium">Finding the best restaurants for you...</p>
        <p className="text-sm text-gray-500 mt-2">This may take a few seconds</p>
      </div>
    </div>
  )
}
