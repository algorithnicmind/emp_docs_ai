"use client";

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Document } from '@/types';
import { Button } from '@/components/ui/Button';
import { Loader2, RefreshCw, Upload, Trash2, FileText, CheckCircle, XCircle, Clock } from 'lucide-react';
import { format } from 'date-fns';

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchDocuments = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.get('/documents');
      // API returns { documents: [], total: ... }
      setDocuments(res.data.documents || []);
    } catch (err) {
      console.error(err);
      setError('Failed to load documents.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'indexed': return <CheckCircle size={16} className="text-green-500" />;
      case 'processing': return <Loader2 size={16} className="text-blue-500 animate-spin" />;
      case 'failed': return <XCircle size={16} className="text-red-500" />;
      default: return <Clock size={16} className="text-zinc-400" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">Documents</h1>
          <p className="text-sm text-zinc-500">Manage indexed knowledge sources.</p>
        </div>
        <div className="flex gap-2">
           <Button variant="outline" size="sm" onClick={fetchDocuments} isLoading={loading}>
             <RefreshCw size={16} className="mr-2" /> Refresh
           </Button>
           <Button size="sm">
             <Upload size={16} className="mr-2" /> Upload
           </Button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-600 rounded-md border border-red-200 text-sm">
          {error}
        </div>
      )}

      <div className="bg-white dark:bg-zinc-900 rounded-lg border dark:border-zinc-800 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-zinc-50 dark:bg-zinc-800/50 border-b dark:border-zinc-800 text-zinc-500">
              <tr>
                <th className="px-6 py-3 font-medium">Title</th>
                <th className="px-6 py-3 font-medium">Source</th>
                <th className="px-6 py-3 font-medium">Status</th>
                <th className="px-6 py-3 font-medium">Department</th>
                <th className="px-6 py-3 font-medium">Chunks</th>
                <th className="px-6 py-3 font-medium">Date</th>
                <th className="px-6 py-3 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y dark:divide-zinc-800">
              {loading && documents.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-8 text-center text-zinc-500">
                    <Loader2 className="h-6 w-6 animate-spin mx-auto mb-2" />
                    Loading documents...
                  </td>
                </tr>
              ) : documents.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-zinc-500">
                    <div className="flex flex-col items-center">
                       <FileText size={32} className="mb-2 opacity-50" />
                       <p>No documents found.</p>
                    </div>
                  </td>
                </tr>
              ) : (
                documents.map((doc) => (
                  <tr key={doc.id} className="hover:bg-zinc-50/50 dark:hover:bg-zinc-800/50 transition-colors">
                    <td className="px-6 py-4 font-medium text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
                      <FileText size={16} className="text-zinc-400" />
                      {doc.title}
                    </td>
                    <td className="px-6 py-4 text-zinc-600 dark:text-zinc-400 capitalize">{doc.source}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 w-fit text-xs font-medium">
                        {getStatusIcon(doc.status)}
                        <span className="capitalize">{doc.status}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 capitalize">{doc.department}</td>
                    <td className="px-6 py-4">{doc.chunk_count}</td>
                    <td className="px-6 py-4 text-zinc-500 whitespace-nowrap">
                      {doc.created_at ? format(new Date(doc.created_at), 'MMM d, yyyy') : '-'}
                    </td>
                    <td className="px-6 py-4 text-right">
                       <button className="text-zinc-400 hover:text-red-600 transition-colors">
                         <Trash2 size={16} />
                       </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
