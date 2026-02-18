import type { Metadata } from 'next';
import { Sidebar } from '@/components/layout/Sidebar'; // Client Component

export const metadata: Metadata = {
  title: 'Dashboard - Internal Docs Q&A',
};

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen overflow-hidden bg-white dark:bg-zinc-950">
      {/* Sidebar - hidden on mobile (for now) but visible on md+ */}
      <div className="hidden md:flex border-r dark:border-zinc-800">
        <Sidebar />
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Mobile Header (TODO: implement mobile nav toggle) */}
        <header className="md:hidden border-b p-4 bg-white dark:bg-zinc-900 flex items-center justify-between">
            <span className="font-bold">Internal Docs</span>
            {/* Menu icon here */}
        </header>

        <main className="flex-1 overflow-y-auto bg-zinc-50/50 dark:bg-zinc-900/50 p-4 md:p-8">
          <div className="mx-auto max-w-7xl h-full">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
