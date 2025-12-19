import ChatInterface from "@/components/ChatInterface";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-24 bg-slate-950 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-black selection:bg-blue-500/30">
      <div className="mb-10 text-center space-y-4">
        <h1 className="text-5xl font-extrabold bg-gradient-to-br from-white via-slate-200 to-slate-500 bg-clip-text text-transparent tracking-tight">
          Support Brain
        </h1>
        <p className="text-slate-400 text-lg font-light max-w-lg mx-auto">
          Smart techincal assistant powered by <span className="text-blue-400 font-medium">RAG</span> and official manuals.
        </p>
      </div>

      <ChatInterface />  
    </main>
  );
}
