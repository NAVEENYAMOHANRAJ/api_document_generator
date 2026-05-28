"use client";

interface ScanResultsProps {
  results: {
    status: string;
    framework_candidates?: string[];
    backend_files?: string[] | number;
    total_candidate_files?: number;
    processed_files?: number;
    failed_files?: number;
    spec_files_detected?: number;
    spec_endpoints_extracted?: number;
    spec_files?: string[];
    duplicates_removed?: number;
    total_unique_endpoints?: number;
    total_endpoints?: number;
    tree_truncated?: boolean;
    total_tree_entries?: number;
    documentation_summary?: {
      endpoints_with_path_params?: number;
      endpoints_with_query_params?: number;
      endpoints_with_headers?: number;
      endpoints_with_request_body?: number;
      endpoints_with_response_model?: number;
      endpoints_with_error_responses?: number;
    };
    extraction_metrics?: Record<string, any>;
    ai_enhancement_summary?: {
      enabled?: boolean;
      mode?: string;
      model?: string;
      enhanced_endpoints?: number;
      message?: string;
    };
    openapi_document?: {
      paths?: Record<string, unknown>;
    };
    markdown_document?: string;
    html_document?: string;
    endpoints?: Array<{
      method?: string;
      path?: string;
      confidence?: number;
      source?: Record<string, any>;
      provenance?: {
        framework?: string;
      };
    }>;
    production_documentation?: Record<string, any>;
    metadata?: Record<string, any>;
  };
}

export default function ScanResults({ results }: ScanResultsProps) {
  const backendFilesCount = typeof results.backend_files === "number" 
    ? results.backend_files 
    : (Array.isArray(results.backend_files) ? results.backend_files.length : results.total_candidate_files || 0);
  
  const endpointCount = results.total_unique_endpoints || results.total_endpoints || 0;
  const duplicatesRemoved = results.duplicates_removed || 0;
  const openApiPathCount = results.openapi_document?.paths
    ? Object.keys(results.openapi_document.paths).length
    : 0;

  // Extract frameworks from endpoints provenance
  const extractedFrameworks = new Set<string>();
  if (results.endpoints && Array.isArray(results.endpoints)) {
    results.endpoints.forEach((ep) => {
      if (ep.provenance?.framework) {
        extractedFrameworks.add(ep.provenance.framework);
      }
    });
  }

  // Combine framework candidates with extracted frameworks
  const allFrameworks = new Set<string>([
    ...(results.framework_candidates || []),
    ...Array.from(extractedFrameworks),
  ]);

  const renderSafeValue = (val: any, fallback: string = "-"): React.ReactNode => {
    if (val === null || val === undefined) return fallback;
    if (typeof val === "object") {
      try {
        return JSON.stringify(val);
      } catch {
        return "[Object]";
      }
    }
    return String(val);
  };

  const downloadFile = (content: string, filename: string, type: string) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  };

  const downloadOpenApiJson = () => {
    if (!results.openapi_document) return;

    downloadFile(
      JSON.stringify(results.openapi_document, null, 2),
      "openapi-generated.json",
      "application/json"
    );
  };

  const downloadMarkdown = () => {
    if (!results.markdown_document) return;
    downloadFile(results.markdown_document, "api-documentation.md", "text/markdown");
  };

  const downloadHtml = () => {
    if (!results.html_document) return;
    downloadFile(results.html_document, "api-documentation.html", "text/html");
  };

  return (
    <div className="mt-8 rounded-lg border border-blue-100 bg-white p-6 shadow-sm">
      <h2 className="text-2xl font-bold text-slate-950 mb-6">Extraction Results</h2>

      {/* Tree Truncation Warning */}
      {results.tree_truncated && (
        <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">
            <strong>Warning:</strong> Repository tree was truncated by GitHub API. Extraction may be incomplete.
          </p>
        </div>
      )}

      {/* Main Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="text-sm text-slate-600">Backend Files</p>
          <p className="text-3xl font-bold text-blue-600">{backendFilesCount}</p>
        </div>
        <div className="bg-sky-50 p-4 rounded-lg">
          <p className="text-sm text-slate-600">Processed</p>
          <p className="text-3xl font-bold text-sky-700">{results.processed_files || 0}</p>
        </div>
        <div className="bg-red-50 p-4 rounded-lg">
          <p className="text-sm text-slate-600">Failed</p>
          <p className="text-3xl font-bold text-red-600">{results.failed_files || 0}</p>
        </div>
        <div className="bg-orange-50 p-4 rounded-lg">
          <p className="text-sm text-slate-600">Duplicates</p>
          <p className="text-3xl font-bold text-orange-600">{duplicatesRemoved}</p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <p className="text-sm text-slate-600">Unique Endpoints</p>
          <p className="text-3xl font-bold text-purple-600">{endpointCount}</p>
        </div>
      </div>

      {(results.spec_files_detected || results.spec_endpoints_extracted) ? (
        <div className="mb-6 bg-blue-50 rounded-lg p-4">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h3 className="text-sm font-semibold text-blue-950">
                OpenAPI/Swagger Specs
              </h3>
              <p className="text-sm text-blue-800">
                {results.spec_files_detected || 0} spec files detected, {results.spec_endpoints_extracted || 0} endpoints extracted from specs.
              </p>
            </div>
            <span className="bg-blue-700 text-white text-xs font-semibold px-3 py-1 rounded">
              Technology-independent
            </span>
          </div>
          {results.spec_files && results.spec_files.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {results.spec_files.map((file) => (
                <span key={file} className="bg-white text-blue-800 text-xs px-2 py-1 rounded border border-blue-200">
                  {file}
                </span>
              ))}
            </div>
          )}
        </div>
      ) : null}

      {/* Repository Stats */}
      {results.total_tree_entries !== undefined && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">
            Total repository tree entries: <span className="font-semibold">{results.total_tree_entries}</span>
          </p>
        </div>
      )}

      {results.ai_enhancement_summary && (
        <div className="mb-6 bg-indigo-50 rounded-lg p-4">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h3 className="text-sm font-semibold text-indigo-900">
                AI Documentation Enrichment
              </h3>
              <p className="text-sm text-indigo-800">
                {results.ai_enhancement_summary.message}
              </p>
            </div>
            <span className="bg-indigo-700 text-white text-xs font-semibold px-3 py-1 rounded">
              {results.ai_enhancement_summary.mode || "off"}
            </span>
          </div>
          <p className="mt-2 text-xs text-indigo-700">
            Enhanced endpoints: {results.ai_enhancement_summary.enhanced_endpoints || 0}
            {results.ai_enhancement_summary.model ? ` | Model: ${results.ai_enhancement_summary.model}` : ""}
          </p>
        </div>
      )}

      {results.documentation_summary && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Documentation Coverage
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            <div className="bg-blue-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600">Path Params</p>
              <p className="text-xl font-bold text-blue-700">{results.documentation_summary.endpoints_with_path_params || 0}</p>
            </div>
            <div className="bg-cyan-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600">Query Params</p>
              <p className="text-xl font-bold text-cyan-700">{results.documentation_summary.endpoints_with_query_params || 0}</p>
            </div>
            <div className="bg-sky-50 p-3 rounded-lg">
              <p className="text-xs text-slate-600">Bodies</p>
              <p className="text-xl font-bold text-sky-700">{results.documentation_summary.endpoints_with_request_body || 0}</p>
            </div>
            <div className="bg-violet-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600">Response Models</p>
              <p className="text-xl font-bold text-violet-700">{results.documentation_summary.endpoints_with_response_model || 0}</p>
            </div>
            <div className="bg-orange-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600">Error Responses</p>
              <p className="text-xl font-bold text-orange-700">{results.documentation_summary.endpoints_with_error_responses || 0}</p>
            </div>
            <div className="bg-slate-100 p-3 rounded-lg">
              <p className="text-xs text-gray-600">Headers</p>
              <p className="text-xl font-bold text-slate-700">{results.documentation_summary.endpoints_with_headers || 0}</p>
            </div>
          </div>
          {openApiPathCount > 0 && (
            <div className="mt-3 bg-gray-50 rounded-lg p-3 flex items-center justify-between gap-3">
              <p className="text-sm text-gray-700">
                Documentation generated with <span className="font-semibold">{openApiPathCount}</span> documented paths.
              </p>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={downloadOpenApiJson}
                  className="px-3 py-2 bg-gray-900 text-white text-sm font-medium rounded hover:bg-gray-800"
                >
                  JSON
                </button>
                <button
                  type="button"
                  onClick={downloadMarkdown}
                  disabled={!results.markdown_document}
                  title={!results.markdown_document ? "Backend response did not include Markdown. Restart backend and extract again." : "Export Markdown documentation"}
                  className={`px-3 py-2 text-sm font-medium rounded ${
                    results.markdown_document
                      ? "bg-blue-700 text-white hover:bg-blue-800"
                      : "bg-gray-200 text-gray-500 cursor-not-allowed"
                  }`}
                >
                  Markdown
                </button>
                <button
                  type="button"
                  onClick={downloadHtml}
                  disabled={!results.html_document}
                  title={!results.html_document ? "Backend response did not include HTML. Restart backend and extract again." : "Export HTML documentation"}
                  className={`px-3 py-2 text-sm font-medium rounded ${
                    results.html_document
                      ? "bg-slate-900 text-white hover:bg-slate-800"
                      : "bg-gray-200 text-gray-500 cursor-not-allowed"
                  }`}
                >
                  HTML
                </button>
              </div>
            </div>
          )}
          {openApiPathCount > 0 && (!results.markdown_document || !results.html_document) && (
            <p className="mt-2 text-xs text-orange-700">
              Markdown/HTML are missing from the API response. Restart the backend server and run extraction again.
            </p>
          )}
        </div>
      )}

      {results.production_documentation && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Production Documentation
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            <div className="bg-emerald-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600">Authentication</p>
              <p className="text-xl font-bold text-emerald-700">
                {(results.production_documentation.authentication as any[])?.length || 0}
              </p>
            </div>
            <div className="bg-indigo-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600">Schemas</p>
              <p className="text-xl font-bold text-indigo-700">
                {Object.keys(results.production_documentation.schemas || {}).length}
              </p>
            </div>
            <div className="bg-cyan-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600">Environments</p>
              <p className="text-xl font-bold text-cyan-700">
                {(results.production_documentation.environments as any[])?.length || 0}
              </p>
            </div>
            <div className="bg-rose-50 p-3 rounded-lg">
              <p className="text-xs text-gray-600">Errors</p>
              <p className="text-xl font-bold text-rose-700">
                {Object.keys(results.production_documentation.errors || {}).length}
              </p>
            </div>
          </div>
          <div className="mt-3 bg-slate-50 rounded-lg p-3 text-sm text-slate-700">
            <span className="font-semibold">OpenAPI:</span>{" "}
            {(results.production_documentation.api as any)?.openapi_version || "3.1.0"}
            <span className="mx-2 text-slate-300">|</span>
            <span className="font-semibold">Version:</span>{" "}
            {(results.production_documentation.api as any)?.version || "1.0.0"}
            <span className="mx-2 text-slate-300">|</span>
            <span className="font-semibold">Rate limit:</span>{" "}
            {(results.production_documentation.rateLimits as any)?.limit ||
              (results.production_documentation.rate_limits as any)?.limit ||
              "N/A"}
          </div>
        </div>
      )}

      {results.extraction_metrics && (
        <>
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Extraction Metrics
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {Object.entries(results.extraction_metrics)
                .filter(([_, val]) => typeof val === "number" || typeof val === "string" || typeof val === "boolean")
                .map(([key, value]) => (
                  <div key={key} className="bg-blue-50 p-3 rounded-lg">
                    <p className="text-xs text-slate-600 font-medium capitalize">
                      {key.split("_").join(" ")}
                    </p>
                    <p className="text-xl font-bold text-blue-700">
                      {typeof value === "boolean" ? (value ? "Yes" : "No") : value}
                    </p>
                  </div>
                ))}
            </div>
          </div>

          {results.extraction_metrics.unresolved_handler_details && 
           Array.isArray(results.extraction_metrics.unresolved_handler_details) && 
           results.extraction_metrics.unresolved_handler_details.length > 0 && (
            <div className="mb-6">
              <details className="border border-amber-200 bg-amber-50 rounded-lg overflow-hidden" open>
                <summary className="cursor-pointer font-semibold text-sm text-amber-950 p-4 select-none hover:bg-amber-100/50 flex items-center justify-between">
                  <span>Unresolved Handler Details ({results.extraction_metrics.unresolved_handler_details.length})</span>
                  <span className="text-xs text-amber-700 font-normal">Click to collapse</span>
                </summary>
                <div className="p-4 border-t border-amber-200 bg-white max-h-60 overflow-y-auto">
                  <table className="min-w-full text-xs text-slate-700 text-left border-collapse">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-500 font-medium">
                        <th className="py-2 pr-2">File</th>
                        <th className="py-2 px-2">Line</th>
                        <th className="py-2 px-2">Handler</th>
                        <th className="py-2 px-2">Stage</th>
                        <th className="py-2 pl-2">Reason</th>
                      </tr>
                    </thead>
                    <tbody>
                      {results.extraction_metrics.unresolved_handler_details.map((item: any, idx: number) => {
                        if (!item || typeof item !== "object") return null;
                        return (
                          <tr key={idx} className="border-b border-slate-100 last:border-0 hover:bg-slate-50">
                            <td className="py-2 pr-2 font-mono truncate max-w-[200px]" title={typeof item.file === "string" ? item.file : ""}>
                              {renderSafeValue(item.file)}
                            </td>
                            <td className="py-2 px-2">{renderSafeValue(item.line)}</td>
                            <td className="py-2 px-2 font-mono">{renderSafeValue(item.handler)}</td>
                            <td className="py-2 px-2 capitalize">{renderSafeValue(item.resolution_stage)}</td>
                            <td className="py-2 pl-2 text-slate-600">{renderSafeValue(item.reason)}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </details>
            </div>
          )}

          {results.extraction_metrics.unsupported_pattern_details && 
           Array.isArray(results.extraction_metrics.unsupported_pattern_details) && 
           results.extraction_metrics.unsupported_pattern_details.length > 0 && (
            <div className="mb-6">
              <details className="border border-red-200 bg-red-50 rounded-lg overflow-hidden" open>
                <summary className="cursor-pointer font-semibold text-sm text-red-950 p-4 select-none hover:bg-red-100/50 flex items-center justify-between">
                  <span>Unsupported Pattern Details ({results.extraction_metrics.unsupported_pattern_details.length})</span>
                  <span className="text-xs text-red-700 font-normal">Click to collapse</span>
                </summary>
                <div className="p-4 border-t border-red-200 bg-white max-h-60 overflow-y-auto">
                  <table className="min-w-full text-xs text-slate-700 text-left border-collapse">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-500 font-medium">
                        <th className="py-2 pr-2">File</th>
                        <th className="py-2 px-2">Line</th>
                        <th className="py-2 px-2">Pattern</th>
                        <th className="py-2 pl-2">Reason</th>
                      </tr>
                    </thead>
                    <tbody>
                      {results.extraction_metrics.unsupported_pattern_details.map((item: any, idx: number) => {
                        if (!item || typeof item !== "object") return null;
                        return (
                          <tr key={idx} className="border-b border-slate-100 last:border-0 hover:bg-slate-50">
                            <td className="py-2 pr-2 font-mono truncate max-w-[200px]" title={typeof item.file === "string" ? item.file : ""}>
                              {renderSafeValue(item.file)}
                            </td>
                            <td className="py-2 px-2">{renderSafeValue(item.line)}</td>
                            <td className="py-2 px-2 font-mono">{renderSafeValue(item.pattern)}</td>
                            <td className="py-2 pl-2 text-slate-600">{renderSafeValue(item.reason)}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </details>
            </div>
          )}
        </>
      )}

      {/* Detected Frameworks */}
      {(results.framework_candidates && results.framework_candidates.length > 0 || extractedFrameworks.size > 0) && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Detected Frameworks
          </h3>
          <div className="flex flex-wrap gap-2">
            {Array.from(allFrameworks).map((framework) => (
              <span
                key={framework}
                className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium"
              >
                {framework}
              </span>
            ))}
          </div>
          {extractedFrameworks.size > 0 && (
            <p className="text-xs text-gray-600 mt-2">
              ✓ Frameworks extracted from {results.endpoints?.length || 0} endpoints
            </p>
          )}
        </div>
      )}

      {/* Backend Files List */}
      {Array.isArray(results.backend_files) && results.backend_files.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Backend Files ({results.backend_files.length})
          </h3>
          <div className="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
            <ul className="space-y-2">
              {results.backend_files.slice(0, 20).map((file) => (
                <li key={file} className="text-sm text-gray-700 font-mono">
                  {file}
                </li>
              ))}
              {results.backend_files.length > 20 && (
                <li className="text-sm text-gray-500 italic">
                  ... and {results.backend_files.length - 20} more
                </li>
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
