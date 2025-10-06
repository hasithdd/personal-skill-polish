'use client'

import { useState } from 'react'
import { ChevronDown, ChevronUp, Award, BookOpen } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Phase {
  id: number
  title: string
  goal: string
  progress: number
  xp: number
  order: number
  notes?: string
  topics: Topic[]
}

interface Topic {
  id: number
  name: string
  progress: number
  xp: number
  subtopics: Subtopic[]
  mastery_components: MasteryComponent[]
}

interface Subtopic {
  id: number
  name: string
  completed: number
  xp: number
}

interface MasteryComponent {
  id: number
  name: string
  level: number
}

interface PhasesListProps {
  phases: Phase[]
  onUpdate: () => void
}

export default function PhasesList({ phases, onUpdate }: PhasesListProps) {
  const [expandedPhases, setExpandedPhases] = useState<Set<number>>(new Set())
  const [expandedTopics, setExpandedTopics] = useState<Set<number>>(new Set())

  const togglePhase = (phaseId: number) => {
    const newExpanded = new Set(expandedPhases)
    if (newExpanded.has(phaseId)) {
      newExpanded.delete(phaseId)
    } else {
      newExpanded.add(phaseId)
    }
    setExpandedPhases(newExpanded)
  }

  const toggleTopic = (topicId: number) => {
    const newExpanded = new Set(expandedTopics)
    if (newExpanded.has(topicId)) {
      newExpanded.delete(topicId)
    } else {
      newExpanded.add(topicId)
    }
    setExpandedTopics(newExpanded)
  }

  const getCompletionBadge = (completed: number) => {
    const badges = [
      { label: 'Not Started', color: 'bg-gray-500' },
      { label: 'In Progress', color: 'bg-yellow-500' },
      { label: 'Completed', color: 'bg-green-500' }
    ]
    return badges[completed] || badges[0]
  }

  const getMasteryColor = (level: number) => {
    if (level === 0) return 'bg-gray-300'
    if (level <= 2) return 'bg-yellow-400'
    if (level <= 4) return 'bg-blue-400'
    return 'bg-purple-400'
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-foreground mb-4">Learning Phases</h2>
      
      {phases
        .sort((a, b) => a.order - b.order)
        .map((phase) => (
          <div key={phase.id} className="bg-card rounded-lg shadow border">
            {/* Phase Header */}
            <div
              className="p-6 cursor-pointer hover:bg-accent/50 transition-colors"
              onClick={() => togglePhase(phase.id)}
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-semibold text-muted-foreground">
                      Phase {phase.order}
                    </span>
                    <h3 className="text-xl font-bold text-foreground">{phase.title}</h3>
                    <div className="flex items-center gap-1 text-yellow-500">
                      <Award className="h-4 w-4" />
                      <span className="text-sm font-medium">{phase.xp} XP</span>
                    </div>
                  </div>
                  <p className="text-muted-foreground mt-1">{phase.goal}</p>
                  
                  {/* Progress Bar */}
                  <div className="mt-3">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-muted-foreground">Progress</span>
                      <span className="text-sm font-semibold text-foreground">
                        {phase.progress.toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-secondary rounded-full h-2">
                      <div
                        className={cn(
                          "h-2 rounded-full transition-all",
                          phase.progress >= 100 ? "bg-green-500" : "bg-primary"
                        )}
                        style={{ width: `${Math.min(phase.progress, 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
                
                <div className="ml-4">
                  {expandedPhases.has(phase.id) ? (
                    <ChevronUp className="h-6 w-6 text-muted-foreground" />
                  ) : (
                    <ChevronDown className="h-6 w-6 text-muted-foreground" />
                  )}
                </div>
              </div>
            </div>

            {/* Phase Content */}
            {expandedPhases.has(phase.id) && (
              <div className="px-6 pb-6 space-y-4">
                {phase.notes && (
                  <div className="bg-accent/30 rounded p-3">
                    <p className="text-sm text-foreground"><strong>Notes:</strong> {phase.notes}</p>
                  </div>
                )}

                {/* Topics */}
                <div className="space-y-3">
                  <h4 className="font-semibold text-foreground flex items-center gap-2">
                    <BookOpen className="h-5 w-5" />
                    Topics ({phase.topics.length})
                  </h4>
                  
                  {phase.topics.map((topic) => (
                    <div key={topic.id} className="border rounded-lg bg-background">
                      <div
                        className="p-4 cursor-pointer hover:bg-accent/30 transition-colors"
                        onClick={() => toggleTopic(topic.id)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <h5 className="font-medium text-foreground">{topic.name}</h5>
                              <span className="text-xs text-yellow-500">{topic.xp} XP</span>
                            </div>
                            <div className="mt-2 flex items-center gap-2">
                              <div className="flex-1 bg-secondary rounded-full h-1.5">
                                <div
                                  className="bg-blue-500 h-1.5 rounded-full"
                                  style={{ width: `${Math.min(topic.progress, 100)}%` }}
                                />
                              </div>
                              <span className="text-xs text-muted-foreground">
                                {topic.progress.toFixed(0)}%
                              </span>
                            </div>
                          </div>
                          {expandedTopics.has(topic.id) ? (
                            <ChevronUp className="h-5 w-5 text-muted-foreground" />
                          ) : (
                            <ChevronDown className="h-5 w-5 text-muted-foreground" />
                          )}
                        </div>
                      </div>

                      {/* Topic Details */}
                      {expandedTopics.has(topic.id) && (
                        <div className="px-4 pb-4 space-y-3">
                          {/* Subtopics */}
                          {topic.subtopics.length > 0 && (
                            <div>
                              <h6 className="text-sm font-semibold text-foreground mb-2">
                                Subtopics
                              </h6>
                              <div className="space-y-1">
                                {topic.subtopics.map((subtopic) => {
                                  const badge = getCompletionBadge(subtopic.completed)
                                  return (
                                    <div
                                      key={subtopic.id}
                                      className="flex items-center justify-between text-sm bg-accent/20 rounded px-3 py-2"
                                    >
                                      <span className="text-foreground">{subtopic.name}</span>
                                      <div className="flex items-center gap-2">
                                        <span className="text-xs text-yellow-500">
                                          {subtopic.xp} XP
                                        </span>
                                        <span
                                          className={cn(
                                            "text-xs px-2 py-1 rounded-full text-white",
                                            badge.color
                                          )}
                                        >
                                          {badge.label}
                                        </span>
                                      </div>
                                    </div>
                                  )
                                })}
                              </div>
                            </div>
                          )}

                          {/* Mastery Components */}
                          {topic.mastery_components.length > 0 && (
                            <div>
                              <h6 className="text-sm font-semibold text-foreground mb-2">
                                Mastery Components
                              </h6>
                              <div className="space-y-2">
                                {topic.mastery_components.map((mastery) => (
                                  <div
                                    key={mastery.id}
                                    className="bg-accent/20 rounded px-3 py-2"
                                  >
                                    <div className="flex items-center justify-between mb-1">
                                      <span className="text-sm text-foreground">
                                        {mastery.name}
                                      </span>
                                      <span className="text-xs text-muted-foreground">
                                        Level {mastery.level}/5
                                      </span>
                                    </div>
                                    <div className="flex gap-1">
                                      {[...Array(5)].map((_, i) => (
                                        <div
                                          key={i}
                                          className={cn(
                                            "flex-1 h-2 rounded",
                                            i < mastery.level
                                              ? getMasteryColor(mastery.level)
                                              : "bg-gray-300"
                                          )}
                                        />
                                      ))}
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
    </div>
  )
}
