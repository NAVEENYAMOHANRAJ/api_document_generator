"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { API, API_ORIGIN } from "@/lib/apiBase";
import RepositoryForm from "@/components/RepositoryForm";
import ScanResults from "@/components/ScanResults";
import EndpointsList from "@/components/EndpointsList";
import EndpointDetailPanel from "@/components/EndpointDetailPanel";
import ProjectDocOverview from "@/components/ProjectDocOverview";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

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
  const [method, setMethod] = useState<string>("ALL");

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
      if (method !== "ALL" && m !== method) return false;
      if (!q) return true;
      const hay = `${m} ${ep?.path || ""} ${ep?.source_file || ""} ${ep?.function_name || ""} ${ep?.description || ""}`.toLowerCase();
      return hay.includes(q);
    });
  }, [endpoints, method, search]);

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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="sticky top-0 z-40 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto max-w-7xl px-6 py-6 flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-slate-950">API Documentation Dashboard</h1>
            <p className="mt-1 text-sm text-slate-600">
              Source-grounded extraction with provenance, confidence, and exports.
            </p>
          </div>
          <div className="flex items-center gap-2">
            {job?.job?.status ? (
              <Badge className="bg-slate-900 text-white">{job.job.status}</Badge>
            ) : (
              <Badge variant="secondary">idle</Badge>
            )}
            {jobId ? <Badge variant="secondary">job: {jobId.slice(0, 8)}</Badge> : null}
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-6 py-8 space-y-6">
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
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">
            {error}
          </div>
        ) : null}

        {scan ? <ScanResults results={scan} /> : null}

        {job ? (
          <Tabs defaultValue="endpoints">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="endpoints">Endpoints</TabsTrigger>
              <TabsTrigger value="metrics">Metrics</TabsTrigger>
              <TabsTrigger value="exports">Exports</TabsTrigger>
              <TabsTrigger value="raw">Raw</TabsTrigger>
            </TabsList>

            <TabsContent value="endpoints" className="space-y-4">
              {endpoints.length === 0 ? (
                <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
                  No endpoints in the current result yet. Use <strong>Generate API Docs</strong> (not only Scan Repository),
                  then wait for job status <strong>completed</strong>.
                </div>
              ) : null}
              <Card>
                <CardHeader className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <CardTitle>Endpoint Catalog</CardTitle>
                    <div className="mt-1 text-sm text-slate-600">
                      {filteredEndpoints.length} shown / {endpoints.length} total
                    </div>
                  </div>
                  <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
                    <Input
                      value={search}
                      onChange={(e) => setSearch(e.target.value)}
                      placeholder="Search path, handler, file…"
                      className="sm:w-[320px]"
                    />
                    <select
                      value={method}
                      onChange={(e) => setMethod(e.target.value)}
                      className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
                    >
                      {methods.map((m) => (
                        <option key={m} value={m}>
                          {m}
                        </option>
                      ))}
                    </select>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                    <div>
                      <ProjectDocOverview
                        endpoints={endpoints as any[]}
                        jobMetadata={jobMeta}
                        documentationSummary={(jobMeta?.documentation_summary || null) as any}
                      />
                      <EndpointsList
                        endpoints={filteredEndpoints}
                        selectedKey={selectedKey}
                        onSelect={(ep, key) => {
                          setSelectedEndpoint(ep);
                          setSelectedKey(key);
                        }}
                      />
                    </div>
                    <div>
                      <EndpointDetailPanel
                        endpoint={selectedEndpoint}
                        openapi={openapi}
                        jobMetadata={jobMeta}
                        baseUrl={baseUrl}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="metrics" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Extraction Metrics</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
                    <div className="rounded-lg border border-slate-200 bg-white p-4">
                      <div className="text-xs text-slate-500">Total endpoints</div>
                      <div className="mt-1 text-2xl font-bold text-slate-950">
                        {job.job.total_endpoints ?? endpoints.length}
                      </div>
                    </div>
                    <div className="rounded-lg border border-slate-200 bg-white p-4">
                      <div className="text-xs text-slate-500">Processed files</div>
                      <div className="mt-1 text-2xl font-bold text-slate-950">{job.job.processed_files}</div>
                    </div>
                    <div className="rounded-lg border border-slate-200 bg-white p-4">
                      <div className="text-xs text-slate-500">Failed files</div>
                      <div className="mt-1 text-2xl font-bold text-slate-950">{job.job.failed_files}</div>
                    </div>
                    <div className="rounded-lg border border-slate-200 bg-white p-4">
                      <div className="text-xs text-slate-500">Status</div>
                      <div className="mt-1 text-2xl font-bold text-slate-950">{job.job.status}</div>
                    </div>
                  </div>

                  {extractionResult ? <ScanResults results={extractionResult} /> : null}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="exports" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Exports</CardTitle>
                </CardHeader>
                <CardContent className="flex flex-wrap gap-3">
                  <Button
                    disabled={!docs?.openapi_spec}
                    onClick={() =>
                      downloadBlob(
                        JSON.stringify(docs?.openapi_spec, null, 2),
                        "openapi.json",
                        "application/json"
                      )
                    }
                  >
                    Download OpenAPI JSON
                  </Button>
                  <Button
                    variant="outline"
                    disabled={!docs?.markdown_doc}
                    onClick={() =>
                      downloadBlob(docs?.markdown_doc || "", "api-docs.md", "text/markdown")
                    }
                  >
                    Download Markdown
                  </Button>
                  <Button
                    variant="outline"
                    disabled={!docs?.html_doc}
                    onClick={() => downloadBlob(docs?.html_doc || "", "api-docs.html", "text/html")}
                  >
                    Download HTML
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="raw" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Raw Job JSON</CardTitle>
                </CardHeader>
                <CardContent>
                  <pre className="max-h-[520px] overflow-auto rounded-lg border border-slate-200 bg-slate-950 p-4 text-xs text-slate-100">
                    {JSON.stringify(job, null, 2)}
                  </pre>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        ) : null}
      </div>
    </div>
  );
}

