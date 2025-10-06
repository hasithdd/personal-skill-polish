'use client'

import { useEffect, useState } from 'react'
import Dashboard from '@/components/Dashboard'
import PhasesList from '@/components/PhasesList'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [phases, setPhases] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [phasesRes, statsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/phases`),
        fetch(`${API_BASE_URL}/api/stats`)
      ])
      
      const phasesData = await phasesRes.json()
      const statsData = await statsRes.json()
      
      setPhases(phasesData)
      setStats(statsData)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto py-8">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            Personal Skill Polish Tracker
          </h1>
          <p className="text-muted-foreground">
            AI/ML System Design Roadmap - From Strong Python Developer → AI Systems Architect
          </p>
        </header>

        {stats && <Dashboard stats={stats} phases={phases} />}
        
        <div className="mt-8">
          <PhasesList phases={phases} onUpdate={fetchData} />
        </div>
      </div>
    </main>
  )
}
