export function Header() {
  return (
    <header className="bg-white border-b border-gray-200 py-4 px-8">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-8">
          <h1 className="text-3xl font-bold text-red-500">zomato</h1>
          <div className="hidden md:flex items-center gap-4">
            <div className="flex items-center gap-2 text-gray-700">
              <span className="text-red-500">📍</span>
              <span className="text-sm">Bengaluru</span>
            </div>
            <input
              type="text"
              placeholder="Search for restaurant, cuisine or a dish"
              className="px-4 py-2 border border-gray-300 rounded-lg text-sm w-64 focus:outline-none focus:border-gray-400"
            />
          </div>
        </div>
        <div className="text-gray-700 text-sm cursor-pointer hover:text-gray-900">Log in</div>
      </div>
    </header>
  )
}
