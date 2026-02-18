"use client";

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Stats } from '@/types';
import { 
  FileText, 
  MessageSquare, 
  Users, 
  Star,
  Activity,
  Loader2,
  LucideIcon
} from 'lucide-react';

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      try {
        const { data } = await api.get('/admin/stats');
        setStats(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="h-8 w-8 animate-spin text-zinc-400" />
      </div>
    );
  }

  if (!stats) return <div className="p-8 text-center text-red-500">Failed to load stats. Ensure backend is running.</div>;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">Admin Dashboard</h1>
        <p className="text-sm text-zinc-500">System overview and analytics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total Documents" value={stats.total_documents} icon={FileText} />
        <StatCard title="Total Queries" value={stats.total_queries} icon={MessageSquare} />
        <StatCard title="Total Users" value={stats.total_users} icon={Users} />
        <StatCard title="Avg Rating" value={Number(stats.avg_feedback_score?.toFixed(1) || 0)} icon={Star} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-zinc-900 p-6 rounded-lg border dark:border-zinc-800">
           <div className="flex items-center gap-2 mb-4 text-zinc-900 dark:text-zinc-100 font-semibold">
              <Activity size={18} className="text-indigo-500" />
              <h2>System Health</h2>
           </div>
           <div className="space-y-4 text-sm text-zinc-600 dark:text-zinc-400">
              <div className="flex justify-between p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-md">
                 <span>Total Chunks Indexed</span>
                 <span className="font-mono font-medium text-zinc-900 dark:text-zinc-100">{stats.total_chunks.toLocaleString()}</span>
              </div>
              <div className="flex justify-between p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-md">
                 <span>Avg Response Time</span>
                 <span className="font-mono font-medium text-zinc-900 dark:text-zinc-100">{stats.avg_response_time_ms} ms</span>
              </div>
              {/* Could add CPU/Memory usage if API provided it */}
           </div>
        </div>

        {/* Placeholder for Recent Activity or Top Queries */}
        <div className="bg-white dark:bg-zinc-900 p-6 rounded-lg border dark:border-zinc-800 flex items-center justify-center text-zinc-400 text-sm">
           More analytics coming soon...
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon }: { title: string, value: number, icon: LucideIcon }) {
  return (
    <div className="bg-white dark:bg-zinc-900 p-6 rounded-lg border dark:border-zinc-800 shadow-sm flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-zinc-500">{title}</p>
        <p className="text-2xl font-bold mt-1 text-zinc-900 dark:text-zinc-100">{value?.toLocaleString() || 0}</p>
      </div>
      <div className="p-3 bg-indigo-50 dark:bg-indigo-900/20 rounded-full text-indigo-600 dark:text-indigo-400">
        <Icon size={20} />
      </div>
    </div>
  );
}
