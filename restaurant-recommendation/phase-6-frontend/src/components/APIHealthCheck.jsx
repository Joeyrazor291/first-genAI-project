export function APIHealthCheck({ status }) {
  const getStatusDisplay = () => {
    switch (status) {
      case 'online':
        return { text: 'Online', className: 'bg-green-100 text-green-800' }
      case 'offline':
        return { text: 'Offline', className: 'bg-red-100 text-red-800' }
      case 'degraded':
        return { text: 'Degraded', className: 'bg-yellow-100 text-yellow-800' }
      default:
        return { text: 'Checking...', className: 'bg-gray-100 text-gray-800' }
    }
  }

  const { text, className } = getStatusDisplay()

  return (
    <span className={`inline-block px-3 py-1 rounded-full font-semibold text-sm ${className}`}>
      {text}
    </span>
  )
}
