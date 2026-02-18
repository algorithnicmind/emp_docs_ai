"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { cn } from '@/lib/utils';
import { 
  MessageSquare, 
  Files, 
  LayoutDashboard, 
  Settings, 
  LogOut, 
  Brain,
  User 
} from 'lucide-react';
import { Button } from '@/components/ui/Button';

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const isAdmin = user?.role === 'admin';

  const links = [
    { href: '/dashboard', label: 'Chat', icon: MessageSquare },
    { href: '/dashboard/documents', label: 'Documents', icon: Files },
  ];

  if (isAdmin) {
    links.push({ href: '/dashboard/admin', label: 'Admin', icon: LayoutDashboard });
  }

  return (
    <div className="flex flex-col h-full border-r bg-zinc-50 dark:bg-zinc-900 w-64">
      {/* Brand */}
      <div className="flex items-center gap-2 p-6 border-b dark:border-zinc-800">
        <div className="p-1 bg-indigo-600 rounded-lg text-white">
          <Brain size={20} />
        </div>
        <span className="font-bold text-lg tracking-tight">Internal Docs</span>
      </div>

      {/* Nav */}
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href;
          
          return (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                isActive 
                  ? "bg-indigo-50 text-indigo-700 dark:bg-indigo-900/20 dark:text-indigo-400" 
                  : "text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-50"
              )}
            >
              <Icon size={18} />
              {link.label}
            </Link>
          );
        })}
      </nav>

      {/* User */}
      <div className="p-4 border-t dark:border-zinc-800">
        <div className="flex items-center gap-3 mb-4 px-2">
          <div className="h-8 w-8 rounded-full bg-zinc-200 flex items-center justify-center text-zinc-500">
            <User size={16} />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.name}</p>
            <p className="text-xs text-zinc-500 truncate">{user?.email}</p>
          </div>
        </div>
        
        <Button 
          variant="ghost" 
          className="w-full justify-start text-zinc-500 hover:text-red-600 hover:bg-red-50"
          onClick={logout}
        >
          <LogOut size={16} className="mr-2" />
          Logout
        </Button>
      </div>
    </div>
  );
}
