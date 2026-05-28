"use client";

export default function DashboardPage() {
  // Deprecated route (used to render synthetic dashboard data).
  // Keep the page but point users to the main dashboard.
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-8">
      <div className="max-w-xl rounded-lg border border-slate-200 bg-white p-6 text-center">
        <h1 className="text-xl font-semibold text-slate-950">Dashboard moved</h1>
        <p className="mt-2 text-sm text-slate-600">
          This page previously rendered synthetic demo documentation. The new dashboard is now the home page.
        </p>
        <a
          href="/"
          className="mt-4 inline-block rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
        >
          Go to dashboard
        </a>
      </div>
    </div>
  );
}
