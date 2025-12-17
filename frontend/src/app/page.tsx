import { Bot } from 'lucide-react';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-slate-900 text-white">
      <div className="bg-slate-800 p-8 rounded-2xl border border-slate-7000 shadow-xl text-center max-w-md">
        <div className="flex justify-center mb-4">
          <div className="p-4 bg-blue-600 rounded-full animate-bounce">
            <Bot size={48} className="text-white" />
          </div>
        </div>

        <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
          Suport Brain
        </h1>

        <p className="text-slate-400 mb-6">
          Stack: Next.js + TypeScript + Tailwind
        </p>

        <div className="px-4 py-2 bg-slate-950/50 rounded border border-slate-700 text-sm font-mono text-emerald-400">
          Frontend System: ONLINE
        </div>
      </div>
    </main>
  )
}
