"use client";

import { useMemo } from "react";
import type { EndpointGroup, EndpointLike } from "@/components/smart/EndpointGrouping";
import { endpointKey, groupEndpoints } from "@/components/smart/EndpointGrouping";

type Props = {
  endpoints: EndpointLike[];
  search: string;
  onSearch: (v: string) => void;
  selectedKey: string | null;
  onSelect: (ep: EndpointLike, key: string) => void;
};

function matches(ep: EndpointLike, q: string): boolean {
  if (!q) return true;
  const hay = `${String(ep.method || "")} ${String(ep.path || "")} ${String(ep.function_name || "")} ${String(ep.source_file || "")}`.toLowerCase();
  return hay.includes(q);
}

export default function EndpointSidebar({ endpoints, search, onSearch, selectedKey, onSelect }: Props) {
  const groups: EndpointGroup[] = useMemo(() => {
    const q = search.trim().toLowerCase();
    const filtered = endpoints.filter((e) => matches(e, q));
    return groupEndpoints(filtered);
  }, [endpoints, search]);

  return (
    <aside className="w-[340px] shrink-0 border-r border-slate-800 bg-slate-950/60">
      <div className="sticky top-0 z-20 border-b border-slate-800 bg-slate-950/80 p-4 backdrop-blur">
        <div className="flex items-center gap-2">
          <div className="h-9 w-9 rounded-xl bg-indigo-500/20 ring-1 ring-indigo-400/30" />
          <div>
            <div className="text-sm font-semibold">Smart API Docs</div>
            <div className="text-xs text-slate-400">Source-grounded</div>
          </div>
        </div>

        <div className="mt-4">
          <input
            value={search}
            onChange={(e) => onSearch(e.target.value)}
            placeholder="Search endpoints…"
            className="w-full rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
          />
        </div>
      </div>

      <div className="p-3">
        <div className="mb-2 px-2 text-[11px] font-semibold tracking-wide text-slate-400">
          ENDPOINTS
        </div>

        {groups.length === 0 ? (
          <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-3 text-sm text-slate-400">
            No endpoints found.
          </div>
        ) : null}

        <div className="space-y-3">
          {groups.map((g) => (
            <Group key={g.id} group={g} selectedKey={selectedKey} onSelect={onSelect} />
          ))}
        </div>
      </div>
    </aside>
  );
}

function Group({
  group,
  selectedKey,
  onSelect,
}: {
  group: EndpointGroup;
  selectedKey: string | null;
  onSelect: (ep: EndpointLike, key: string) => void;
}) {
  return (
    <div>
      <div className="flex items-center justify-between px-2 py-1 text-xs font-semibold text-slate-300">
        <span>{group.title}</span>
        <span className="rounded-full bg-slate-900 px-2 py-0.5 text-[11px] text-slate-400 ring-1 ring-slate-800">
          {group.endpoints.length}
        </span>
      </div>
      <div className="mt-1 space-y-1">
        {group.endpoints.map((ep) => {
          const key = endpointKey(ep);
          const selected = !!selectedKey && key === selectedKey;
          const method = String(ep.method || "GET").toUpperCase();
          const path = String(ep.path || "/");
          return (
            <button
              key={key}
              onClick={() => onSelect(ep, key)}
              className={`flex w-full items-center gap-2 rounded-lg px-2 py-2 text-left text-sm ring-1 ${
                selected
                  ? "bg-indigo-500/15 text-slate-100 ring-indigo-400/30"
                  : "bg-transparent text-slate-200 ring-transparent hover:bg-slate-900/50 hover:ring-slate-800"
              }`}
            >
              <span className={`w-12 shrink-0 rounded-md px-2 py-0.5 text-[11px] font-bold ${methodPill(method)}`}>
                {method}
              </span>
              <span className="truncate font-mono text-[12px] text-slate-200">{path}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

function methodPill(method: string): string {
  switch (method) {
    case "GET":
      return "bg-sky-500/15 text-sky-300 ring-1 ring-sky-400/20";
    case "POST":
      return "bg-emerald-500/15 text-emerald-300 ring-1 ring-emerald-400/20";
    case "PUT":
    case "PATCH":
      return "bg-amber-500/15 text-amber-300 ring-1 ring-amber-400/20";
    case "DELETE":
      return "bg-rose-500/15 text-rose-300 ring-1 ring-rose-400/20";
    default:
      return "bg-slate-700/40 text-slate-200 ring-1 ring-slate-600/30";
  }
}

