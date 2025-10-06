import { useEffect, useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

interface Topic {
  id: number;
  name: string;
  description: string;
  order: number;
}

interface Phase {
  id: number;
  name: string;
  description: string;
  order: number;
}

export default function PhaseDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [phase, setPhase] = useState<Phase | null>(null);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchPhaseAndTopics();
    }
  }, [id]);

  const fetchPhaseAndTopics = async () => {
    try {
      const [phaseRes, topicsRes] = await Promise.all([
        axios.get(`/api/phases/${id}`),
        axios.get(`/api/topics?phase_id=${id}`)
      ]);
      setPhase(phaseRes.data);
      setTopics(topicsRes.data);
    } catch (error) {
      console.error('Error fetching phase details:', error);
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

  if (!phase) {
    return <div className="text-center text-gray-500">Phase not found</div>;
  }

  return (
    <div className="px-4 sm:px-0">
      <button
        onClick={() => router.push('/phases')}
        className="mb-4 text-blue-600 hover:text-blue-800 flex items-center"
      >
        <svg
          className="h-5 w-5 mr-1"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 19l-7-7 7-7"
          />
        </svg>
        Back to Phases
      </button>

      <div className="card mb-8">
        <div className="flex items-center space-x-3 mb-4">
          <span className="inline-flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 text-blue-600 font-bold text-lg">
            {phase.order}
          </span>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{phase.name}</h1>
            <p className="text-gray-600 mt-1">{phase.description}</p>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Topics ({topics.length})
        </h2>
      </div>

      <div className="space-y-4">
        {topics.map((topic) => (
          <div key={topic.id} className="card">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="badge badge-info">{topic.order}</span>
                  <h3 className="text-xl font-semibold text-gray-900">
                    {topic.name}
                  </h3>
                </div>
                <p className="text-gray-600">{topic.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {topics.length === 0 && (
        <div className="text-center text-gray-500 py-8">
          No topics available for this phase yet.
        </div>
      )}
    </div>
  );
}
