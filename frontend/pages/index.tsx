import { useEffect, useState } from 'react';
import axios from 'axios';

interface Stats {
  total_points: number;
  total_hours: number;
  current_streak: number;
  longest_streak: number;
  phases_completed: number;
  topics_completed: number;
  subtopics_completed: number;
}

interface PhaseSummary {
  id: number;
  name: string;
  total_topics: number;
  completed_topics: number;
  progress_percentage: number;
}

interface Achievement {
  id: number;
  name: string;
  description: string;
  icon: string;
  points: number;
  unlocked: boolean;
}

interface DashboardData {
  stats: Stats;
  phases_summary: PhaseSummary[];
  achievements: Achievement[];
}

export default function Home() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await axios.get('/api/dashboard');
      setDashboardData(response.data);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="text-center text-gray-500">
        Failed to load dashboard data
      </div>
    );
  }

  const { stats, phases_summary, achievements } = dashboardData;

  return (
    <div className="px-4 sm:px-0">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        AI/ML System Design Roadmap Dashboard
      </h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="text-4xl">🎯</div>
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Total Points
                </dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {stats.total_points}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="text-4xl">⏱️</div>
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Total Hours
                </dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {stats.total_hours}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="text-4xl">🔥</div>
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Current Streak
                </dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {stats.current_streak} days
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="text-4xl">✅</div>
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Subtopics Done
                </dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {stats.subtopics_completed}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      {/* Phase Progress */}
      <div className="card mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Phase Progress</h2>
        <div className="space-y-4">
          {phases_summary.map((phase) => (
            <div key={phase.id}>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">
                  {phase.name}
                </span>
                <span className="text-sm text-gray-500">
                  {phase.completed_topics}/{phase.total_topics} topics
                </span>
              </div>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${phase.progress_percentage}%` }}
                ></div>
              </div>
              <div className="text-right text-xs text-gray-500 mt-1">
                {phase.progress_percentage.toFixed(1)}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Achievements */}
      {achievements.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            🏆 Unlocked Achievements
          </h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {achievements.map((achievement) => (
              <div
                key={achievement.id}
                className="flex items-center space-x-3 p-3 bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-lg border border-yellow-200"
              >
                <div className="text-3xl">{achievement.icon}</div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">
                    {achievement.name}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {achievement.description}
                  </p>
                  <p className="text-xs text-yellow-700 font-medium mt-1">
                    +{achievement.points} points
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
