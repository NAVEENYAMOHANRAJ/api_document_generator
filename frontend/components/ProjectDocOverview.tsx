"use client";

import { useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { detectApiVersion, getFramework, hasPagination, inferAuth } from "@/lib/endpointDoc";

type Props = {
  endpoints: Record<string, unknown>[];
  jobMetadata?: Record<string, unknown> | null;
  documentationSummary?: Record<string, unknown> | null;
};

export default function ProjectDocOverview({ endpoints, jobMetadata, documentationSummary }: Props) {
  const stats = useMemo(() => {
    const frameworks = new Set<string>();
    let withAuth = 0;
    let withBody = 0;
    let withErrors = 0;
    let withMiddleware = 0;
    let withPagination = 0;
    const versions = new Set<string>();

    for (const ep of endpoints) {
      const fw = getFramework(ep);
      if (fw) frameworks.add(fw);
      if (inferAuth(ep)) withAuth += 1;
      if (ep.request_body || ep.requestBody) withBody += 1;
      const responses = (ep.responses as unknown[]) || [];
      if (responses.some((r) => Number((r as Record<string, unknown>)?.status_code) >= 400)) withErrors += 1;
      if ((ep.middleware as unknown[])?.length) withMiddleware += 1;
      if (hasPagination(ep)) withPagination += 1;
      const v = detectApiVersion(String(ep.path ?? ""));
      if (v) versions.add(v);
    }

    return {
      total: endpoints.length,
      frameworks: Array.from(frameworks),
      withAuth,
      withBody,
      withErrors,
      withMiddleware,
      withPagination,
      versions: Array.from(versions),
    };
  }, [endpoints]);

  const metrics = (jobMetadata?.extraction_metrics ?? {}) as Record<string, unknown>;
  const summary = documentationSummary || (jobMetadata?.documentation_summary as Record<string, unknown>) || {};

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>API documentation overview</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <Stat label="Endpoints" value={stats.total} />
          <Stat label="With auth (detected)" value={stats.withAuth} />
          <Stat label="With request body" value={stats.withBody} />
          <Stat label="With error responses" value={stats.withErrors} />
          <Stat label="With middleware" value={stats.withMiddleware} />
          <Stat label="With pagination params" value={stats.withPagination} />
          <Stat label="Frameworks" value={stats.frameworks.join(", ") || "—"} />
          <Stat label="API versions in paths" value={stats.versions.join(", ") || "—"} />
        </CardContent>
      </Card>

      {Object.keys(summary).length > 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>Extraction coverage</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="max-h-48 overflow-auto rounded-md border bg-slate-50 p-3 text-xs">
              {JSON.stringify(summary, null, 2)}
            </pre>
          </CardContent>
        </Card>
      ) : null}

      {Object.keys(metrics).length > 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>Pipeline metrics</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="max-h-48 overflow-auto rounded-md border bg-slate-50 p-3 text-xs">
              {JSON.stringify(metrics, null, 2)}
            </pre>
          </CardContent>
        </Card>
      ) : null}

    </div>
  );
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-lg border border-slate-200 p-3">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-1 text-lg font-bold text-slate-900">{value}</div>
    </div>
  );
}
