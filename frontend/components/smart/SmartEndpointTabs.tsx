"use client";

import { useMemo } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import {
  buildCurl,
  codeExamples,
  errorResponses,
  getHeaders,
  getMiddleware,
  getPathParams,
  getQueryParams,
  getRequestBody,
  getResponses,
  getSecurity,
  inferAuth,
  mergeOpenApiIntoEndpoint,
  notDetected,
  statusCodes,
  successResponses,
  validationRulesFromBody,
} from "@/lib/endpointDoc";

function Json({ value }: { value: unknown }) {
  if (value == null) return <p className="text-sm text-slate-400 italic">{notDetected()}</p>;
  return (
    <pre className="max-h-[420px] overflow-auto rounded-lg border border-slate-800 bg-slate-950 p-4 text-xs text-slate-100">
      {JSON.stringify(value, null, 2)}
    </pre>
  );
}

export default function SmartEndpointTabs({
  endpoint,
  openapi,
  baseUrl,
}: {
  endpoint: any | null;
  openapi: any | null;
  baseUrl: string;
}) {
  const ep = useMemo(() => {
    if (!endpoint) return null;
    return mergeOpenApiIntoEndpoint(endpoint, openapi ?? null);
  }, [endpoint, openapi]);

  if (!ep) {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-8 text-center text-sm text-slate-400">
        Select an endpoint on the left.
      </div>
    );
  }

  const method = String(ep.method ?? "GET").toUpperCase();
  const path = String(ep.path ?? "/");
  const auth = inferAuth(ep);
  const security = getSecurity(ep);
  const middleware = getMiddleware(ep);
  const pathParams = getPathParams(ep);
  const queryParams = getQueryParams(ep);
  const headers = getHeaders(ep);
  const body = getRequestBody(ep);
  const validation = validationRulesFromBody(body);
  const responses = getResponses(ep);
  const codes = statusCodes(ep);
  const ok = successResponses(ep);
  const errs = errorResponses(ep);
  const curl = (ep.curl_example as string) || buildCurl(ep, baseUrl);
  const examples = codeExamples(ep, baseUrl);

  return (
    <div className="space-y-4">
      <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-5">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-md bg-indigo-500/15 px-2 py-1 text-xs font-bold text-indigo-200 ring-1 ring-indigo-400/20">
            {method}
          </span>
          <code className="text-sm font-semibold text-slate-100">{path}</code>
          <Badge className="bg-emerald-500/15 text-emerald-200 ring-1 ring-emerald-400/20">Active</Badge>
        </div>

        <div className="mt-3 flex flex-wrap gap-2">
          {auth ? (
            <Badge className="bg-slate-900 text-slate-200 ring-1 ring-slate-800">
              Requires Auth
            </Badge>
          ) : (
            <Badge className="bg-slate-900 text-slate-400 ring-1 ring-slate-800">
              No auth detected
            </Badge>
          )}
          {security.length ? (
            <Badge className="bg-slate-900 text-slate-200 ring-1 ring-slate-800">
              Security: {security.length}
            </Badge>
          ) : null}
          {middleware.length ? (
            <Badge className="bg-slate-900 text-slate-200 ring-1 ring-slate-800">
              Middleware: {middleware.length}
            </Badge>
          ) : null}
          {codes.length ? (
            <Badge className="bg-slate-900 text-slate-200 ring-1 ring-slate-800">
              Status codes: {codes.join(", ")}
            </Badge>
          ) : null}
        </div>
      </div>

      <Tabs defaultValue="overview">
        <TabsList className="grid w-full grid-cols-6 bg-slate-950/30">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="parameters">Parameters</TabsTrigger>
          <TabsTrigger value="request">Request</TabsTrigger>
          <TabsTrigger value="responses">Responses</TabsTrigger>
          <TabsTrigger value="examples">Examples</TabsTrigger>
          <TabsTrigger value="code">Code Samples</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <CardGrid>
            <InfoCard title="Authentication" value={auth ? auth.summary : notDetected("Not found")} />
            <InfoCard title="Content Type" value="application/json" />
            <InfoCard title="Response Type" value="application/json" />
            <InfoCard title="Middleware" value={middleware.length ? middleware.join(", ") : notDetected("Not found")} />
          </CardGrid>
          <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
            <div className="text-xs font-semibold text-slate-300">Provenance</div>
            <div className="mt-2">
              <Json value={ep.provenance ?? null} />
            </div>
          </div>
        </TabsContent>

        <TabsContent value="parameters" className="space-y-4">
          <TwoCol
            left={
              <Panel title={`Path Parameters (${pathParams.length})`}>
                <Json value={pathParams.length ? pathParams : null} />
              </Panel>
            }
            right={
              <Panel title={`Query Parameters (${queryParams.length})`}>
                <Json value={queryParams.length ? queryParams : null} />
              </Panel>
            }
          />
          <Panel title={`Headers (${headers.length})`}>
            <Json value={headers.length ? headers : null} />
          </Panel>
        </TabsContent>

        <TabsContent value="request" className="space-y-4">
          <Panel title="Request Body">
            <Json value={body} />
          </Panel>
          <Panel title={`Validation Rules (${validation.length})`}>
            <Json value={validation.length ? validation : null} />
          </Panel>
        </TabsContent>

        <TabsContent value="responses" className="space-y-4">
          <TwoCol
            left={
              <Panel title={`Success Responses (${ok.length})`}>
                <Json value={ok.length ? ok : null} />
              </Panel>
            }
            right={
              <Panel title={`Error Responses (${errs.length})`}>
                <Json value={errs.length ? errs : null} />
              </Panel>
            }
          />
          <Panel title="All responses">
            <Json value={responses.length ? responses : null} />
          </Panel>
        </TabsContent>

        <TabsContent value="examples" className="space-y-4">
          <Panel title="cURL">
            <pre className="overflow-auto rounded-lg border border-slate-800 bg-slate-950 p-4 text-xs text-emerald-100 whitespace-pre-wrap">
              {curl}
            </pre>
          </Panel>
        </TabsContent>

        <TabsContent value="code" className="space-y-4">
          {Object.entries(examples).map(([lang, code]) => (
            <Panel key={lang} title={lang}>
              <pre className="overflow-auto rounded-lg border border-slate-800 bg-slate-950 p-4 text-xs text-slate-100 whitespace-pre-wrap">
                {code}
              </pre>
            </Panel>
          ))}
        </TabsContent>
      </Tabs>
    </div>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
      <div className="text-xs font-semibold text-slate-300">{title}</div>
      <div className="mt-3">{children}</div>
    </div>
  );
}

function TwoCol({ left, right }: { left: React.ReactNode; right: React.ReactNode }) {
  return <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">{left}{right}</div>;
}

function CardGrid({ children }: { children: React.ReactNode }) {
  return <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">{children}</div>;
}

function InfoCard({ title, value }: { title: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
      <div className="text-xs text-slate-400">{title}</div>
      <div className="mt-1 text-sm font-semibold text-slate-100">{value}</div>
    </div>
  );
}

