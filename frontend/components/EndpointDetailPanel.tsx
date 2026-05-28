"use client";

import { useMemo } from "react";
import DocFeatureSection from "@/components/DocFeatureSection";
import { InteractiveTestingPanel } from "@/components/InteractiveTestingPanel";
import {
  buildCurl,
  codeExamples,
  detectApiVersion,
  errorResponses,
  getFramework,
  getHeaders,
  getMiddleware,
  getPathParams,
  getQueryParams,
  getRequestBody,
  getResponses,
  getSecurity,
  hasPagination,
  inferAuth,
  mergeOpenApiIntoEndpoint,
  notDetected,
  statusCodes,
  successResponses,
  validationRulesFromBody,
  type DocEndpoint,
} from "@/lib/endpointDoc";

function JsonBlock({ value }: { value: unknown }) {
  if (value == null) {
    return <p className="text-slate-500 italic">{notDetected()}</p>;
  }
  return (
    <pre className="max-h-48 overflow-auto rounded-md bg-slate-950 p-3 text-xs text-slate-100">
      {JSON.stringify(value, null, 2)}
    </pre>
  );
}

function ParamTable({ params }: { params: unknown[] }) {
  if (!params.length) {
    return <p className="text-slate-500 italic">{notDetected()}</p>;
  }
  return (
    <table className="w-full text-xs">
      <thead>
        <tr className="border-b text-left text-slate-500">
          <th className="py-1 pr-2">Name</th>
          <th className="py-1 pr-2">In</th>
          <th className="py-1">Details</th>
        </tr>
      </thead>
      <tbody>
        {params.map((p, i) => {
          const row = (p || {}) as Record<string, unknown>;
          return (
            <tr key={i} className="border-b border-slate-100">
              <td className="py-1.5 pr-2 font-mono">{String(row.name ?? "—")}</td>
              <td className="py-1.5 pr-2">{String(row.in ?? row.location ?? "—")}</td>
              <td className="py-1.5">
                <JsonBlock value={row.schema ?? row.type ?? row} />
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

type Props = {
  endpoint: DocEndpoint | null;
  openapi?: Record<string, unknown> | null;
  jobMetadata?: Record<string, unknown> | null;
  baseUrl?: string;
};

export default function EndpointDetailPanel({
  endpoint,
  openapi,
  jobMetadata,
  baseUrl = "http://localhost:8000",
}: Props) {
  const ep = useMemo(() => {
    if (!endpoint) return null;
    return mergeOpenApiIntoEndpoint(endpoint, openapi ?? null);
  }, [endpoint, openapi]);

  if (!ep) {
    return (
      <div className="flex h-full min-h-[320px] items-center justify-center rounded-lg border border-dashed border-slate-300 bg-slate-50 p-8 text-center text-sm text-slate-600">
        Select an endpoint from the list to view full API documentation features.
      </div>
    );
  }

  const method = String(ep.method ?? "GET").toUpperCase();
  const path = String(ep.path ?? "/");
  const pathParams = getPathParams(ep);
  const queryParams = getQueryParams(ep);
  const headers = getHeaders(ep);
  const body = getRequestBody(ep);
  const responses = getResponses(ep);
  const errors = errorResponses(ep);
  const successes = successResponses(ep);
  const codes = statusCodes(ep);
  const auth = inferAuth(ep);
  const middleware = getMiddleware(ep);
  const validation = validationRulesFromBody(body);
  const version = detectApiVersion(path);
  const pagination = hasPagination(ep);
  const rateLimits = jobMetadata?.rate_limits ?? jobMetadata?.rateLimits;
  const curl = (ep.curl_example as string) || buildCurl(ep, baseUrl);
  const examples = codeExamples(ep, baseUrl);
  const framework = getFramework(ep);
  const provenance = ep.provenance as Record<string, unknown> | undefined;
  const confidence = ep.confidence ?? (ep.confidence_score as number | undefined);

  const responseSchema =
    ep.response_model ||
    successes.find((r) => r.schema || r.model)?.schema ||
    successes.find((r) => r.model)?.model;

  return (
    <div className="space-y-3 max-h-[calc(100vh-220px)] overflow-y-auto pr-1">
      <div className="sticky top-0 z-10 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded bg-slate-900 px-2 py-1 text-xs font-bold text-white">{method}</span>
          <code className="text-sm font-semibold text-slate-900">{path}</code>
        </div>
        {ep.description ? (
          <p className="mt-2 text-sm text-slate-600">{String(ep.description)}</p>
        ) : null}
        <div className="mt-2 flex flex-wrap gap-2 text-xs text-slate-500">
          {framework ? <span>Framework: {framework}</span> : null}
          {ep.source_file ? <span>Source: {String(ep.source_file)}</span> : null}
          {provenance?.line_number != null ? <span>Line: {String(provenance.line_number)}</span> : null}
          {confidence != null ? (
            <span>Confidence: {(Number(confidence) <= 1 ? Number(confidence) * 100 : Number(confidence)).toFixed(0)}%</span>
          ) : null}
        </div>
      </div>

      <DocFeatureSection title="1. Endpoint" description="URL to call" detected>
        <code className="font-mono text-base">
          {method} {path}
        </code>
      </DocFeatureSection>

      <DocFeatureSection title="2. HTTP Method" detected>
        <p>
          <strong>{method}</strong> —{" "}
          {method === "GET"
            ? "Read data"
            : method === "POST"
              ? "Create data"
              : method === "PUT"
                ? "Update full resource"
                : method === "PATCH"
                  ? "Partial update"
                  : method === "DELETE"
                    ? "Remove data"
                    : "HTTP operation"}
        </p>
      </DocFeatureSection>

      <DocFeatureSection title="3. Request Parameters" description="Body / input" detected={!!body}>
        <JsonBlock value={body?.example ?? body?.schema ?? body} />
      </DocFeatureSection>

      <DocFeatureSection title="4. Response Example" detected={successes.length > 0 || !!responseSchema}>
        {successes.length ? (
          <JsonBlock value={successes[0].example ?? successes[0].schema ?? successes[0]} />
        ) : (
          <JsonBlock value={responseSchema ? { model: responseSchema } : null} />
        )}
      </DocFeatureSection>

      <DocFeatureSection title="5. Status Codes" detected={codes.length > 0}>
        {codes.length ? (
          <ul className="list-disc pl-5 space-y-1">
            {codes.map((c) => (
              <li key={c}>
                <strong>{c}</strong> —{" "}
                {String(
                  responses.find((r) => Number(r.status_code) === c)?.description ||
                    (c < 400 ? "Success" : c < 500 ? "Client error" : "Server error")
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p className="italic text-slate-500">{notDetected()}</p>
        )}
      </DocFeatureSection>

      <DocFeatureSection title="6. Authentication" detected={!!auth}>
        {auth ? (
          <div>
            <p className="font-medium">{auth.summary}</p>
            <ul className="mt-1 list-disc pl-5 text-xs text-slate-600">
              {auth.details.map((d) => (
                <li key={d}>{d}</li>
              ))}
            </ul>
            {getSecurity(ep).length === 0 && !auth.summary.includes("Bearer") ? (
              <p className="mt-2 text-xs text-slate-500">No Bearer/JWT header inferred unless detected in middleware.</p>
            ) : null}
          </div>
        ) : (
          <p className="italic text-slate-500">No authentication required (not detected in source)</p>
        )}
      </DocFeatureSection>

      <DocFeatureSection title="7. Headers" detected={headers.length > 0}>
        <ParamTable params={headers} />
      </DocFeatureSection>

      <DocFeatureSection title="8. Query Parameters" detected={queryParams.length > 0}>
        <ParamTable params={queryParams} />
      </DocFeatureSection>

      <DocFeatureSection title="9. Path Parameters" detected={pathParams.length > 0}>
        <ParamTable params={pathParams} />
      </DocFeatureSection>

      <DocFeatureSection title="10. Validation Rules" detected={validation.length > 0}>
        {validation.length ? <JsonBlock value={validation} /> : <p className="italic text-slate-500">{notDetected()}</p>}
      </DocFeatureSection>

      <DocFeatureSection title="11. Error Responses" detected={errors.length > 0}>
        {errors.length ? <JsonBlock value={errors} /> : <p className="italic text-slate-500">{notDetected()}</p>}
      </DocFeatureSection>

      <DocFeatureSection title="12. Example Request (cURL)" detected>
        <pre className="max-h-40 overflow-auto rounded-md bg-slate-950 p-3 text-xs text-emerald-100 whitespace-pre-wrap">
          {curl}
        </pre>
      </DocFeatureSection>

      <DocFeatureSection title="13. Response Schema" detected={!!responseSchema}>
        <JsonBlock value={responseSchema} />
      </DocFeatureSection>

      <DocFeatureSection title="14. API Versioning" detected={!!version}>
        {version ? (
          <p>
            Version prefix: <code className="font-mono">{version}</code>
          </p>
        ) : (
          <p className="italic text-slate-500">{notDetected("No /v1 style prefix in path")}</p>
        )}
      </DocFeatureSection>

      <DocFeatureSection title="15. Rate Limiting" detected={!!rateLimits && Object.keys(rateLimits as object).length > 0}>
        {rateLimits && Object.keys(rateLimits as object).length ? (
          <JsonBlock value={rateLimits} />
        ) : (
          <p className="italic text-slate-500">{notDetected()}</p>
        )}
      </DocFeatureSection>

      <DocFeatureSection title="16. Pagination" detected={pagination}>
        {pagination ? (
          <p>Query parameters suggest pagination: {queryParams.map((q) => String((q as Record<string, unknown>).name)).join(", ")}</p>
        ) : (
          <p className="italic text-slate-500">{notDetected()}</p>
        )}
      </DocFeatureSection>

      <DocFeatureSection title="17. Interactive Testing" detected>
        <InteractiveTestingPanel endpoint={ep} baseUrl={baseUrl} />
      </DocFeatureSection>

      <DocFeatureSection title="18. Middleware" detected={middleware.length > 0}>
        {middleware.length ? (
          <ul className="list-disc pl-5">
            {middleware.map((m) => (
              <li key={m} className="font-mono text-xs">
                {m}
              </li>
            ))}
          </ul>
        ) : (
          <p className="italic text-slate-500">{notDetected()}</p>
        )}
      </DocFeatureSection>

      <DocFeatureSection title="19. Database Relations" detected={false}>
        <p className="italic text-slate-500">{notDetected("ORM relations not extracted yet")}</p>
      </DocFeatureSection>

      <DocFeatureSection title="20. Code Examples" detected>
        {Object.entries(examples).map(([lang, code]) => (
          <div key={lang} className="mb-3">
            <div className="mb-1 text-xs font-semibold text-slate-600">{lang}</div>
            <pre className="overflow-auto rounded-md bg-slate-950 p-3 text-xs text-slate-100 whitespace-pre-wrap">{code}</pre>
          </div>
        ))}
      </DocFeatureSection>

      {provenance ? (
        <DocFeatureSection title="Source provenance" detected>
          <JsonBlock value={provenance} />
        </DocFeatureSection>
      ) : null}
    </div>
  );
}
