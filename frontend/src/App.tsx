import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-center space-y-8 p-8">
        <h1 className="text-4xl font-bold text-foreground">
          SchemaGenius AI
        </h1>
        <p className="text-xl text-muted-foreground">
          From Natural Language to Production-Ready Database Architecture
        </p>

        <div className="space-y-4 pt-8">
          <div className="bg-card border border-border rounded-lg p-6 shadow-sm">
            <p className="text-sm text-muted-foreground mb-4">
              Frontend Health Check
            </p>
            <button
              onClick={() => setCount((count) => count + 1)}
              className="bg-primary text-primary-foreground hover:bg-primary/90 px-6 py-2 rounded-md font-medium transition-colors"
            >
              Count is {count}
            </button>
          </div>

          <div className="text-sm text-muted-foreground">
            <p>✅ React + TypeScript + Vite</p>
            <p>✅ Tailwind CSS configured</p>
            <p>⏳ Backend health check coming next...</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
