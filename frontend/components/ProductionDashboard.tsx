"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { API, API_ORIGIN } from "@/lib/apiBase";
import RepositoryForm from "@/components/RepositoryForm";
import SmartShell from "@/components/smart/SmartShell";
import EndpointSidebar from "@/components/smart/EndpointSidebar";
import TryItOutRail from "@/components/smart/TryItOutRail";
import SmartEndpointTabs from "@/components/smart/SmartEndpointTabs";
import { Button } from "@/components/ui/button";

type JobStatus = "pending" | "processing" | "completed" | "failed";

type ScanResult = any;

type JobDetailsResponse = {
  status: "success";
  job: {
    job_id: string;
    repo_url: string;
    repo_name: string;
    status: JobStatus;
    total_endpoints: number;
    processed_files: number;
    failed_files: number;
    errors: any;
    metadata: any;
    created_at: string;
    completed_at: string | null;
  };
  endpoints: any[];
  documentation: {
    openapi_spec: any;
    markdown_doc: string;
    html_doc: string;
  } | null;
};

type JobsListResponse = {
  status: "success";
  jobs: Array<{
    job_id: string;
    status: JobStatus;
    total_endpoints: number;
    created_at: string;
  }>;
};

function downloadBlob(content: string, filename: string, mime: string) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function alternateApiUrls(url: string): string[] {
  const urls = [url];
  try {
    const parsed = new URL(url);
    if (parsed.port === "8001") {
      parsed.port = "8000";
      urls.push(parsed.toString());
    } else if (parsed.port === "8000") {
      parsed.port = "8001";
      urls.push(parsed.toString());
    }
  } catch {
    // keep original only
  }
  return urls;
}

async function fetchWithPortFallback(url: string, init?: RequestInit): Promise<Response> {
  let lastError: unknown;
  for (const candidate of alternateApiUrls(url)) {
    try {
      const res = await fetch(candidate, init);
      return res;
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError instanceof Error ? lastError : new Error("Backend not reachable on ports 8000/8001");
}

export default function ProductionDashboard() {
  const [scan, setScan] = useState<ScanResult | null>(null);
  const [jobId, setJobId] = useState<string>("");
  const [job, setJob] = useState<JobDetailsResponse | null>(null);
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const [selectedEndpoint, setSelectedEndpoint] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingLabel, setLoadingLabel] = useState<string>("");
  const [error, setError] = useState<string>("");

  const [search, setSearch] = useState("");

  const pollRef = useRef<number | null>(null);

  const stopPolling = () => {
    if (pollRef.current) {
      window.clearInterval(pollRef.current);
      pollRef.current = null;
    }
  };

  const pollJob = async (id: string) => {
    const res = await fetchWithPortFallback(API.jobDetails(id));
    if (!res.ok) throw new Error("Failed to load job");
    const data = (await res.json()) as JobDetailsResponse;
    setJob(data);
    if (!selectedEndpoint && (data?.endpoints?.length || 0) > 0) {
      // auto-select first endpoint after job loads
      const first = data.endpoints[0];
      setSelectedEndpoint(first);
      setSelectedKey(String((first as any)?.id ?? `${first?.method || ""} ${first?.path || ""} ${first?.source_file || ""}`));
    }
    const st = data.job?.status;
    if (st === "completed" || st === "failed") stopPolling();
  };

  const loadLatestCompletedJob = useCallback(async () => {
    try {
      const res = await fetchWithPortFallback(`${API_ORIGIN}/api/jobs?limit=20`);
      if (!res.ok) return;
      const data = (await res.json()) as JobsListResponse;
      const latest =
        data?.jobs?.find((j) => j.status === "completed" && (j.total_endpoints ?? 0) > 0) ||
        data?.jobs?.find((j) => j.status === "completed");
      if (latest?.job_id) {
        await pollJob(latest.job_id);
        setJobId(latest.job_id);
      }
    } catch {
      // Keep dashboard usable even if history endpoint is unavailable.
    }
  }, []);

  useEffect(() => {
    loadLatestCompletedJob();
    return () => stopPolling();
  }, [loadLatestCompletedJob]);

  const startPolling = (id: string) => {
    stopPolling();
    pollRef.current = window.setInterval(() => {
      pollJob(id).catch((e) => setError(e instanceof Error ? e.message : String(e)));
    }, 1500);
  };

  const onCancel = () => {
    stopPolling();
    setLoading(false);
    setLoadingLabel("");
  };

  const onScan = async (repoUrl: string, token: string) => {
    setLoading(true);
    setLoadingLabel("Scanning repository…");
    setError("");
    setScan(null);
    try {
      const res = await fetchWithPortFallback(API.scanRepo, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl, github_token: token || null }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || "Scan failed");
      setScan(data);
    } finally {
      setLoading(false);
      setLoadingLabel("");
    }
  };

  const runExtraction = async (endpoint: string, payload: any) => {
    setLoading(true);
    setLoadingLabel("Starting extraction job…");
    setError("");
    setJob(null);
    setJobId("");
    setSelectedKey(null);
    setSelectedEndpoint(null);
    try {
      const res = await fetchWithPortFallback(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || "Extraction failed");

      if (data?.job_id) {
        setJobId(data.job_id);
        setLoadingLabel("Processing…");
        await pollJob(data.job_id);
        startPolling(data.job_id);
      } else {
        // Synchronous mode (tests / scripts)
        setSelectedEndpoint((data?.endpoints || [])[0] || null);
        setJob({
          status: "success",
          job: {
            job_id: "sync",
            repo_url: payload?.repo_url || payload?.folder_path || payload?.filename || "",
            repo_name: "sync",
            status: "completed",
            total_endpoints: data?.total_unique_endpoints || data?.total_endpoints || 0,
            processed_files: data?.processed_files || 0,
            failed_files: data?.failed_files || 0,
            errors: data?.errors || [],
            metadata: data,
            created_at: new Date().toISOString(),
            completed_at: new Date().toISOString(),
          },
          endpoints: data?.endpoints || [],
          documentation: {
            openapi_spec: data?.openapi_document || null,
            markdown_doc: data?.markdown_document || "",
            html_doc: data?.html_document || "",
          },
        });
      }
    } finally {
      setLoading(false);
      setLoadingLabel("");
    }
  };

  const onExtract = (repoUrl: string, token: string) =>
    runExtraction(API.extractGithub, { repo_url: repoUrl, github_token: token || null });

  const onExtractLocalFolder = (folderPath: string) =>
    runExtraction(API.extractLocal, { folder_path: folderPath });

  const onExtractUpload = async (file: File) => {
    setLoading(true);
    setLoadingLabel("Uploading ZIP…");
    setError("");
    setJob(null);
    setJobId("");
    try {
      const bytes = await file.arrayBuffer();
      const res = await fetchWithPortFallback(`${API.extractUpload}?filename=${encodeURIComponent(file.name)}`, {
        method: "POST",
        headers: { "Content-Type": "application/zip" },
        body: bytes,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || "Upload extraction failed");
      if (data?.job_id) {
        setJobId(data.job_id);
        await pollJob(data.job_id);
        startPolling(data.job_id);
      }
    } finally {
      setLoading(false);
      setLoadingLabel("");
    }
  };

  const extractionMeta = job?.job?.metadata || {};
  const extractionResult = extractionMeta?.documentation_summary ? extractionMeta : null;

  const endpoints = useMemo(() => job?.endpoints || [], [job]);

  const methods = useMemo(() => {
    const set = new Set<string>();
    for (const ep of endpoints) {
      if (ep?.method) set.add(String(ep.method).toUpperCase());
    }
    return ["ALL", ...Array.from(set).sort()];
  }, [endpoints]);

  const filteredEndpoints = useMemo(() => {
    const q = search.trim().toLowerCase();
    return endpoints.filter((ep) => {
      const m = String(ep?.method || "").toUpperCase();
      if (!q) return true;
      const hay = `${m} ${ep?.path || ""} ${ep?.source_file || ""} ${ep?.function_name || ""} ${ep?.description || ""}`.toLowerCase();
      return hay.includes(q);
    });
  }, [endpoints, search]);

  const docs = job?.documentation;
  const openapi = docs?.openapi_spec || null;
  const jobMeta = (job?.job?.metadata || {}) as Record<string, any>;
  const baseUrl =
    jobMeta?.api?.base_url ||
    jobMeta?.api_base_url ||
    jobMeta?.base_url ||
    (process.env.NEXT_PUBLIC_API_BASE_URL as string | undefined) ||
    "http://localhost:8000";

  return (
    <SmartShell>
      <EndpointSidebar
        endpoints={filteredEndpoints}
        search={search}
        onSearch={setSearch}
        selectedKey={selectedKey}
        onSelect={(ep, key) => {
          setSelectedEndpoint(ep);
          setSelectedKey(key);
        }}
      />

      <main className="flex min-w-0 flex-1 flex-col">
        <div className="sticky top-0 z-30 border-b border-slate-800 bg-slate-950/80 backdrop-blur">
          <div className="flex items-center justify-between gap-3 px-6 py-4">
            <div>
              <div className="text-sm font-semibold text-slate-100">API Dashboard</div>
              <div className="text-xs text-slate-400">
                {job?.job?.repo_name ? `Repo: ${job.job.repo_name}` : "Load a repo to extract endpoints"}
              </div>
            </div>
            <div className="flex items-center gap-2">
              {job?.job?.status ? (
                <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-slate-200 ring-1 ring-slate-800">
                  {job.job.status}
                </span>
              ) : (
                <span className="rounded-full bg-slate-900 px-3 py-1 text-xs text-slate-400 ring-1 ring-slate-800">
                  idle
                </span>
              )}
              {docs?.openapi_spec ? (
                <Button
                  variant="outline"
                  className="border-slate-700 bg-slate-950 text-slate-100 hover:bg-slate-900"
                  onClick={() =>
                    downloadBlob(JSON.stringify(docs.openapi_spec, null, 2), "openapi.json", "application/json")
                  }
                >
                  Export JSON
                </Button>
              ) : null}
              {docs?.markdown_doc ? (
                <Button
                  variant="outline"
                  className="border-slate-700 bg-slate-950 text-slate-100 hover:bg-slate-900"
                  onClick={() => downloadBlob(docs.markdown_doc || "", "api-docs.md", "text/markdown")}
                >
                  Export MD
                </Button>
              ) : null}
              {docs?.html_doc ? (
                <Button
                  variant="outline"
                  className="border-slate-700 bg-slate-950 text-slate-100 hover:bg-slate-900"
                  onClick={() => downloadBlob(docs.html_doc || "", "api-docs.html", "text/html")}
                >
                  Export HTML
                </Button>
              ) : null}
            </div>
          </div>

          <div className="px-6 pb-4">
            <RepositoryForm
              onScan={onScan}
              onExtract={onExtract}
              onExtractLocalFolder={onExtractLocalFolder}
              onExtractUpload={onExtractUpload}
              onCancel={onCancel}
              loading={loading || (!!jobId && (job?.job?.status === "processing" || job?.job?.status === "pending"))}
              loadingLabel={loadingLabel || (job?.job?.status === "processing" ? "Processing…" : undefined)}
            />
            {error ? (
              <div className="mt-4 rounded-lg border border-rose-800 bg-rose-950/40 p-3 text-sm text-rose-200">
                {error}
              </div>
            ) : null}
          </div>
        </div>

        <div className="min-w-0 flex-1 p-6">
          <SmartEndpointTabs endpoint={selectedEndpoint} openapi={openapi} baseUrl={baseUrl} />
        </div>
      </main>

      <TryItOutRail endpoint={selectedEndpoint} baseUrl={baseUrl} />
    </SmartShell>
  );
}

