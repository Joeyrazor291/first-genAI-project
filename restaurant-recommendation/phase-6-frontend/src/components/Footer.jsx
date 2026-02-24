import { APIHealthCheck } from './APIHealthCheck'

export function Footer({ apiStatus }) {
  return (
    <footer className="bg-white border-t border-gray-200 mt-12">
      <div className="max-w-7xl mx-auto px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-center md:text-left">
            <p className="text-gray-700 font-semibold mb-1">Powered by AI Restaurant Recommendations</p>
            <p className="text-sm text-gray-600">API Status: <APIHealthCheck status={apiStatus} /></p>
          </div>
          <div className="text-sm text-gray-600">
            Built with ❤️ • All phases integrated and operational
          </div>
        </div>
      </div>
    </footer>
  )
}
