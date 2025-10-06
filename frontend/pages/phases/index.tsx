import { useEffect, useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

interface Phase {
  id: number;
  name: string;
  description: string;
  order: number;
}

export default function Phases() {
  const [phases, setPhases] = useState<Phase[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    fetchPhases();
  }, []);

  const fetchPhases = async () => {
    try {
      const response = await axios.get('/api/phases');
      setPhases(response.data);
    } catch (error) {
      console.error('Error fetching phases:', error);
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

  return (
    <div className="px-4 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          AI/ML Learning Phases
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          Your complete roadmap to mastering AI/ML System Design
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {phases.map((phase) => (
          <div
            key={phase.id}
            className="card cursor-pointer transform hover:scale-105 transition-transform duration-200"
            onClick={() => router.push(`/phases/${phase.id}`)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="inline-flex items-center justify-center h-8 w-8 rounded-full bg-blue-100 text-blue-600 font-bold text-sm">
                    {phase.order}
                  </span>
                  <h2 className="text-xl font-semibold text-gray-900">
                    {phase.name}
                  </h2>
                </div>
                <p className="text-gray-600 mt-2">{phase.description}</p>
              </div>
              <svg
                className="h-5 w-5 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
