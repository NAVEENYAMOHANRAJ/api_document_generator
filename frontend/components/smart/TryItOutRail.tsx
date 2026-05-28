"use client";

import { InteractiveTestingPanel } from "@/components/InteractiveTestingPanel";

export default function TryItOutRail({
  endpoint,
  baseUrl,
}: {
  endpoint: any | null;
  baseUrl: string;
}) {
  return (
    <aside className="w-[420px] shrink-0 border-l border-slate-800 bg-slate-950/40">
      <div className="sticky top-0 z-20 border-b border-slate-800 bg-slate-950/80 p-4 backdrop-blur">
        <div className="text-sm font-semibold">Try It Out</div>
        <div className="text-xs text-slate-400">Send a live request</div>
      </div>

      <div className="p-4">
        {endpoint ? (
          <InteractiveTestingPanel endpoint={endpoint} baseUrl={baseUrl} />
        ) : (
          <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-4 text-sm text-slate-400">
            Select an endpoint to test.
          </div>
        )}
      </div>
    </aside>
  );
}

