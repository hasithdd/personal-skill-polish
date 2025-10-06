'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { TrendingUp, Award, BookOpen, Target } from 'lucide-react'

interface DashboardProps {
  stats: {
    total_phases: number
    completed_phases: number
    total_progress: number
    total_xp: number
    phases_progress: Array<{
      id: number
      title: string
      progress: number
      xp: number
      order: number
    }>
  }
  phases: any[]
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF6B9D', '#C2C2F0', '#FFD700']

export default function Dashboard({ stats, phases }: DashboardProps) {
  const progressData = stats.phases_progress
    .sort((a, b) => a.order - b.order)
    .map(phase => ({
      name: `Phase ${phase.order}`,
      progress: phase.progress,
      xp: phase.xp
    }))

  const completionData = [
    { name: 'Completed', value: stats.completed_phases },
    { name: 'In Progress', value: stats.total_phases - stats.completed_phases }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {/* Stats Cards */}
      <div className="bg-card rounded-lg shadow p-6 border">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-muted-foreground text-sm">Total Progress</p>
            <p className="text-3xl font-bold text-foreground">{stats.total_progress.toFixed(1)}%</p>
          </div>
          <TrendingUp className="h-8 w-8 text-primary" />
        </div>
      </div>

      <div className="bg-card rounded-lg shadow p-6 border">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-muted-foreground text-sm">Total XP</p>
            <p className="text-3xl font-bold text-foreground">{stats.total_xp}</p>
          </div>
          <Award className="h-8 w-8 text-yellow-500" />
        </div>
      </div>

      <div className="bg-card rounded-lg shadow p-6 border">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-muted-foreground text-sm">Completed Phases</p>
            <p className="text-3xl font-bold text-foreground">{stats.completed_phases}/{stats.total_phases}</p>
          </div>
          <Target className="h-8 w-8 text-green-500" />
        </div>
      </div>

      <div className="bg-card rounded-lg shadow p-6 border">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-muted-foreground text-sm">Active Topics</p>
            <p className="text-3xl font-bold text-foreground">{phases.reduce((acc, p) => acc + p.topics.length, 0)}</p>
          </div>
          <BookOpen className="h-8 w-8 text-blue-500" />
        </div>
      </div>

      {/* Progress Chart */}
      <div className="bg-card rounded-lg shadow p-6 border md:col-span-2 lg:col-span-3">
        <h3 className="text-lg font-semibold mb-4 text-foreground">Progress by Phase</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={progressData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="progress" fill="#0088FE" name="Progress %" />
            <Bar dataKey="xp" fill="#00C49F" name="XP" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Completion Pie Chart */}
      <div className="bg-card rounded-lg shadow p-6 border">
        <h3 className="text-lg font-semibold mb-4 text-foreground">Completion Status</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={completionData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: ${entry.value}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {completionData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
