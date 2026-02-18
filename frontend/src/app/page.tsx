"use client";

import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { KeyRound, Mail, Brain, ShieldCheck, Zap, LucideIcon } from 'lucide-react';
import { api } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const { login, user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user && !authLoading) {
      router.push('/dashboard');
    }
  }, [user, authLoading, router]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.post('/auth/login', { email, password });
      const { token, user } = response.data;
      login(token, user);
      router.push('/dashboard');
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        setError('Invalid email or password.');
      } else {
        setError('Something went wrong. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen w-full bg-white dark:bg-zinc-950">
      {/* Left Side: Hero / Branding */}
      <div className="hidden lg:flex flex-col justify-center w-1/2 p-12 bg-zinc-900 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/20 via-purple-600/20 to-zinc-900 z-0" />
        
        <div className="relative z-10 max-w-lg mx-auto">
          <div className="h-16 w-16 bg-white/10 backdrop-blur-md rounded-2xl flex items-center justify-center mb-8 border border-white/20">
            <Brain className="h-8 w-8 text-indigo-400" />
          </div>
          
          <h1 className="text-4xl font-bold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-white to-white/70">
            Internal Knowledge, Instantly Accessible
          </h1>
          
          <p className="text-lg text-zinc-400 mb-8 leading-relaxed">
            Empower your team with AI-driven answers from your internal documentation. 
            Secure, fast, and cited.
          </p>

          <div className="space-y-4">
            <FeatureItem icon={ShieldCheck} title="Enterprise Security" desc="Role-based access control & secure data handling" />
            <FeatureItem icon={Zap} title="Instant Answers" desc="Semantic search powered by advanced LLMs" />
          </div>
        </div>
      </div>

      {/* Right Side: Login Form */}
      <div className="flex-1 flex flex-col justify-center items-center p-8">
        <div className="w-full max-w-sm space-y-6">
          <div className="text-center lg:text-left">
            <h2 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-white">
              Welcome back
            </h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2">
              Sign in to access the Q&A agent and admin dashboard.
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 dark:text-zinc-300">
                Email
              </label>
              <Input
                type="email"
                placeholder="name@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                icon={Mail}
                autoComplete="email"
                required
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 dark:text-zinc-300">
                Password
              </label>
              <Input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                icon={KeyRound}
                autoComplete="current-password"
                required
              />
            </div>

            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md dark:bg-red-900/10 dark:text-red-400 dark:border-red-900/50">
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full bg-indigo-600 hover:bg-indigo-700"
              isLoading={loading}
            >
              Sign In
            </Button>
          </form>

          <div className="px-8 text-center text-xs text-zinc-400">
            For demo access: <span className="font-mono bg-zinc-100 dark:bg-zinc-800 px-1 py-0.5 rounded">admin@company.com</span> / <span className="font-mono bg-zinc-100 dark:bg-zinc-800 px-1 py-0.5 rounded">admin123</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureItem({ icon: Icon, title, desc }: { icon: LucideIcon, title: string, desc: string }) {
  return (
    <div className="flex items-start gap-3">
      <div className="mt-1 p-1.5 bg-indigo-500/10 rounded-lg text-indigo-400">
        <Icon size={18} />
      </div>
      <div>
        <h3 className="font-semibold text-white text-sm">{title}</h3>
        <p className="text-zinc-500 text-xs">{desc}</p>
      </div>
    </div>
  );
}
