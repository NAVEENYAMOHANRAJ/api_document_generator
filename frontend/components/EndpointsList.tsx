"use client";

interface Endpoint {
  framework?: string;
  method: string;
  path: string;
  source_file?: string;
  matched_line?: string;
  function_name?: string;
  router_prefix?: string;
  path_params?: Array<Record<string, unknown>>;
  pathParameters?: Array<Record<string, unknown>>;
  query_params?: Array<Record<string, unknown>>;
  queryParameters?: Array<Record<string, unknown>>;
  headers?: Array<Record<string, unknown>>;
  request_body?: {
    name?: string;
    model?: string;
    schema?: {
      properties?: Record<string, unknown>;
    };
  };
  requestBody?: {
    required?: boolean;
    content_type?: string;
    schema?: {
      properties?: Record<string, unknown>;
      required?: string[];
    };
    example?: Record<string, unknown>;
  };
  responses?: Array<{
    status_code?: number;
    model?: string;
    description?: string;
    message?: string;
    schema?: Record<string, unknown>;
  }>;
  response_model?: string;
  status_code?: number;
  summary?: string;
  description?: string;
  ai_enhanced?: boolean;
  ai_notes?: {
    request?: string;
    response?: string;
    errors?: string;
  };
  confidence?: number;
  confidence_score?: number;
  source?: {
    route_file?: string;
    controller_file?: string;
    method?: string;
    line?: number;
    framework?: string;
  };
  middleware?: string[];
  security?: string[];
  curlExample?: string;
  curl_example?: string;
  requestExample?: Record<string, unknown>;
  request_example?: Record<string, unknown>;
  provenance?: {
    framework?: string;
    source_file?: string;
    detection_type?: string;
    line_number?: number;
  };
}

interface EndpointsListProps {
  endpoints: Endpoint[];
  selectedKey?: string | null;
  onSelect?: (endpoint: Endpoint, key: string) => void;
}

const methodColors: Record<string, string> = {
  GET: "bg-blue-100 text-blue-800",
  POST: "bg-sky-100 text-sky-800",
  PUT: "bg-yellow-100 text-yellow-800",
  DELETE: "bg-red-100 text-red-800",
  PATCH: "bg-purple-100 text-purple-800",
  OPTIONS: "bg-gray-100 text-gray-800",
  HEAD: "bg-gray-100 text-gray-800",
};

const getConfidenceColor = (score?: number): string => {
  if (!score) return "text-gray-500";
  if (score >= 0.8) return "text-blue-700";
  if (score >= 0.6) return "text-yellow-600";
  return "text-orange-600";
};

function endpointKey(endpoint: any): string {
  return String(endpoint?.id ?? `${endpoint?.method || ""} ${endpoint?.path || ""} ${endpoint?.source_file || ""}`);
}

export default function EndpointsList({ endpoints, selectedKey, onSelect }: EndpointsListProps) {
  const getDocSummary = (endpoint: Endpoint) => {
    const queryCount = endpoint.queryParameters?.length || endpoint.query_params?.length || 0;
    const pathCount = endpoint.pathParameters?.length || endpoint.path_params?.length || 0;
    const headerCount = endpoint.headers?.length || 0;
    const bodyModel =
      endpoint.request_body?.model ||
      (endpoint.requestBody?.schema?.properties ? `${Object.keys(endpoint.requestBody.schema.properties).length} fields` : "");
    const responseModel = endpoint.response_model || endpoint.responses?.find((response) => response.model)?.model;
    const responseCodes = endpoint.responses
      ?.map((response) => response.status_code)
      .filter(Boolean)
      .join(", ");

    return {
      queryCount,
      pathCount,
      headerCount,
      bodyModel,
      responseModel,
      responseCodes,
    };
  };

  return (
    <div className="mt-8 rounded-lg border border-blue-100 bg-white p-6 shadow-sm">
      <h2 className="text-2xl font-bold text-slate-950 mb-6">
        Extracted Endpoints ({endpoints.length})
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold text-gray-700">
                Method
              </th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">
                Path
              </th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">
                Framework
              </th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">
                Confidence
              </th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">
                Source File
              </th>
            </tr>
          </thead>
          <tbody>
            {endpoints.map((endpoint, idx) => {
              const summary = getDocSummary(endpoint);
              const confidence = endpoint.confidence_score ?? endpoint.confidence;
              const key = endpointKey(endpoint);
              const selected = !!selectedKey && key === selectedKey;
              return (
                <tr
                  key={key || idx}
                  className={`border-b border-gray-100 hover:bg-gray-50 ${
                    selected ? "bg-blue-50" : ""
                  } ${onSelect ? "cursor-pointer" : ""}`}
                  onClick={() => onSelect?.(endpoint, key)}
                >
                    <td className="py-3 px-4">
                      <span
                        className={`inline-block px-2 py-1 rounded text-xs font-semibold ${
                          methodColors[endpoint.method] || "bg-gray-100 text-gray-800"
                        }`}
                      >
                        {endpoint.method}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-900">
                      <div className="font-mono">{endpoint.path}</div>
                      {endpoint.summary && (
                        <div className="mt-1 text-sm font-medium text-gray-800">
                          {endpoint.summary}
                        </div>
                      )}
                      {endpoint.description && (
                        <div className="mt-1 text-xs text-gray-600">
                          {endpoint.description}
                        </div>
                      )}
                      <div className="mt-2 flex flex-wrap gap-2 text-xs">
                        <span className={`${endpoint.ai_enhanced ? "bg-blue-50 text-blue-700" : "bg-gray-100 text-gray-700"} px-2 py-1 rounded`}>
                          {endpoint.ai_enhanced ? "LLM enhanced" : "rule summary"}
                        </span>
                      {endpoint.function_name && (
                          <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded">
                            handler: {endpoint.function_name}
                          </span>
                        )}
                        {endpoint.middleware && endpoint.middleware.length > 0 && (
                          <span className="bg-slate-100 text-slate-700 px-2 py-1 rounded">
                            middleware: {endpoint.middleware.join(", ")}
                          </span>
                        )}
                        {endpoint.security && endpoint.security.length > 0 && (
                          <span className="bg-emerald-50 text-emerald-700 px-2 py-1 rounded">
                            security: {endpoint.security.join(", ")}
                          </span>
                        )}
                        {summary.pathCount > 0 && (
                          <span className="bg-blue-50 text-blue-700 px-2 py-1 rounded">
                            path params: {summary.pathCount}
                          </span>
                        )}
                        {summary.queryCount > 0 && (
                          <span className="bg-cyan-50 text-cyan-700 px-2 py-1 rounded">
                            query: {summary.queryCount}
                          </span>
                        )}
                        {summary.headerCount > 0 && (
                          <span className="bg-slate-100 text-slate-700 px-2 py-1 rounded">
                            headers: {summary.headerCount}
                          </span>
                        )}
                        {summary.bodyModel && (
                          <span className="bg-sky-50 text-sky-700 px-2 py-1 rounded">
                            body: {summary.bodyModel}
                          </span>
                        )}
                        {summary.responseModel && (
                          <span className="bg-violet-50 text-violet-700 px-2 py-1 rounded">
                            response: {summary.responseModel}
                          </span>
                        )}
                        {summary.responseCodes && (
                          <span className="bg-orange-50 text-orange-700 px-2 py-1 rounded">
                            codes: {summary.responseCodes}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-600">
                      {endpoint.source?.framework || endpoint.provenance?.framework || endpoint.framework || "Unknown"}
                    </td>
                    <td className={`py-3 px-4 text-sm font-semibold ${getConfidenceColor(confidence)}`}>
                      {confidence !== undefined ? `${(confidence * 100).toFixed(0)}%` : "N/A"}
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-600 truncate">
                      {endpoint.source?.route_file || endpoint.source?.controller_file || endpoint.provenance?.source_file || endpoint.source_file || "N/A"}
                      {endpoint.source?.line ? (
                        <span className="block text-xs text-slate-400">line {endpoint.source.line}</span>
                      ) : null}
                    </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-800 mb-2">
          <strong>Confidence Score:</strong> Indicates extraction reliability based on decorator type, router prefix, and path validation.
        </p>
        <p className="text-xs text-blue-700">
          High (80%+) | Medium (60-79%) | Low (&lt;60%)
        </p>
      </div>
    </div>
  );
}
