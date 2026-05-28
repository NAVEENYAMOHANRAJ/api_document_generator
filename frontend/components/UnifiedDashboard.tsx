"use client";

import { useState, useEffect } from "react";
import {
  FileText,
  Lock,
  Globe,
  Zap,
  AlertCircle,
  Code,
  Webhook,
  BookOpen,
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
  Upload,
  Loader,
  GitBranch,
} from "lucide-react";

interface Parameter {
  name: string;
  type: string;
  required: boolean;
  description: string;
  location: string;
}

interface Response {
  status_code: number;
  description: string;
  schema?: any;
}

interface Endpoint {
  method: string;
  path: string;
  summary: string;
  description: string;
  parameters: Parameter[];
  request_body?: any;
  responses: Response[];
  security: string[];
  tags: string[];
  deprecated: boolean;
  source_file: string;
  line_number: number;
  confidence: number;
  handler_class?: string;
  handler_method?: string;
}

interface ExtractionResult {
  status: string;
  framework: string;
  endpoints: Endpoint[];
  statistics: {
    total_endpoints: number;
    methods: Record<string, number>;
    files_scanned: number;
    average_confidence: number;
  };
  metadata: Record<string, any>;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001/api";

export default function UnifiedDashboard() {
  const [source, setSource] = useState("");
  const [extractionResult, setExtractionResult] = useState<ExtractionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [expandedEndpoint, setExpandedEndpoint] = useState<string | null>(null);
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("overview");

  const handleExtract = async () => {
    if (!source.trim()) {
      setError("Please enter a source path or GitHub URL");
      return;
    }

    setLoading(true);
    setError("");
    setExtractionResult(null);

    try {
      // Use Laravel extraction endpoint
      const response = await fetch(`${API_BASE_URL}/extract-laravel`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repo_url: source.trim(),
          github_token: null,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Extraction failed");
      }

      const data = await response.json();
      setExtractionResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/extract-upload?filename=${file.name}`, {
        method: "POST",
        body: file,
        headers: { "Content-Type": "application/zip" },
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      setExtractionResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const getMethodColor = (method: string) => {
    const colors: Record<string, string> = {
      GET: "bg-blue-600",
      POST: "bg-green-600",
      PUT: "bg-yellow-600",
      DELETE: "bg-red-600",
      PATCH: "bg-purple-600",
      OPTIONS: "bg-gray-600",
    };
    return colors[method] || "bg-slate-600";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <h1 className="text-4xl font-bold text-slate-900">API Extraction Dashboard</h1>
          <p className="text-slate-600 mt-2">
            Extract and analyze API endpoints from your source code using AST parsing
          </p>
        </div>
      </div>

      {/* Extraction Form */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="bg-white rounded-lg border border-slate-200 p-8 mb-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-6">Extract Endpoints</h2>

          <div className="space-y-4">
            {/* Source Input */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Source (Local Path or GitHub URL)
              </label>
              <input
                type="text"
                value={source}
                onChange={(e) => setSource(e.target.value)}
                placeholder="e.g., /path/to/project or https://github.com/user/repo"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Buttons */}
            <div className="flex gap-4">
              <button
                onClick={handleExtract}
                disabled={loading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
              >
                {loading ? <Loader className="animate-spin" size={20} /> : <Zap size={20} />}
                Extract
              </button>

              <label className="px-6 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-700 cursor-pointer flex items-center gap-2">
                <Upload size={20} />
                Upload ZIP
                <input
                  type="file"
                  accept=".zip"
                  onChange={handleFileUpload}
                  disabled={loading}
                  className="hidden"
                />
              </label>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {error}
              </div>
            )}
          </div>
        </div>

        {/* Results */}
        {extractionResult && (
          <div className="space-y-8">
            {/* Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white rounded-lg border border-slate-200 p-6">
                <p className="text-sm text-slate-600 font-medium">Total Endpoints</p>
                <p className="text-3xl font-bold text-slate-900 mt-2">
                  {extractionResult.statistics.total_endpoints}
                </p>
              </div>

              <div className="bg-white rounded-lg border border-slate-200 p-6">
                <p className="text-sm text-slate-600 font-medium">Framework</p>
                <p className="text-3xl font-bold text-slate-900 mt-2 capitalize">
                  {extractionResult.framework || "Unknown"}
                </p>
              </div>

              <div className="bg-white rounded-lg border border-slate-200 p-6">
                <p className="text-sm text-slate-600 font-medium">Files Scanned</p>
                <p className="text-3xl font-bold text-slate-900 mt-2">
                  {extractionResult.statistics.files_scanned}
                </p>
              </div>

              <div className="bg-white rounded-lg border border-slate-200 p-6">
                <p className="text-sm text-slate-600 font-medium">Avg Confidence</p>
                <p className="text-3xl font-bold text-slate-900 mt-2">
                  {(extractionResult.statistics.average_confidence * 100).toFixed(0)}%
                </p>
              </div>
            </div>

            {/* HTTP Methods Distribution */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">HTTP Methods</h3>
              <div className="flex gap-4 flex-wrap">
                {Object.entries(extractionResult.statistics.methods).map(([method, count]) => (
                  <div key={method} className="flex items-center gap-2">
                    <span className={`px-3 py-1 rounded text-white font-semibold text-sm ${getMethodColor(method)}`}>
                      {method}
                    </span>
                    <span className="text-slate-600 font-medium">{count}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Endpoints List */}
            <div className="space-y-4">
              <h3 className="text-2xl font-bold text-slate-900">Endpoints</h3>

              {extractionResult.endpoints.map((endpoint, idx) => {
                const endpointId = `${endpoint.method}-${endpoint.path}-${idx}`;
                const isExpanded = expandedEndpoint === endpointId;

                return (
                  <div
                    key={idx}
                    className="bg-white rounded-lg border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors"
                  >
                    <button
                      onClick={() => setExpandedEndpoint(isExpanded ? null : endpointId)}
                      className="w-full p-6 flex items-center justify-between hover:bg-slate-50 transition-colors"
                    >
                      <div className="flex items-center gap-4 flex-1 text-left">
                        <span className={`px-3 py-1 rounded font-semibold text-white text-sm ${getMethodColor(endpoint.method)}`}>
                          {endpoint.method}
                        </span>
                        <div className="flex-1">
                          <p className="font-mono font-semibold text-slate-900">{endpoint.path}</p>
                          <p className="text-sm text-slate-600 mt-1">{endpoint.summary}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-slate-500">{endpoint.source_file}</p>
                          <p className="text-xs text-slate-500">Line {endpoint.line_number}</p>
                          <div className="mt-1">
                            <span className="inline-block px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                              {(endpoint.confidence * 100).toFixed(0)}%
                            </span>
                          </div>
                        </div>
                      </div>
                      {isExpanded ? (
                        <ChevronUp className="text-slate-400" />
                      ) : (
                        <ChevronDown className="text-slate-400" />
                      )}
                    </button>

                    {isExpanded && (
                      <div className="border-t border-slate-200 p-6 bg-slate-50 space-y-6">
                        {endpoint.description && (
                          <div>
                            <h4 className="font-semibold text-slate-900 mb-2">Description</h4>
                            <p className="text-slate-700">{endpoint.description}</p>
                          </div>
                        )}

                        {endpoint.handler_class && (
                          <div>
                            <h4 className="font-semibold text-slate-900 mb-2">Handler</h4>
                            <p className="font-mono text-slate-700">
                              {endpoint.handler_class}@{endpoint.handler_method}
                            </p>
                          </div>
                        )}

                        {endpoint.parameters && endpoint.parameters.length > 0 && (
                          <div>
                            <h4 className="font-semibold text-slate-900 mb-3">Parameters</h4>
                            <div className="space-y-2">
                              {endpoint.parameters.map((param, pidx) => (
                                <div key={pidx} className="p-3 bg-white rounded border border-slate-200">
                                  <div className="flex items-center gap-2">
                                    <span className="font-mono font-semibold text-slate-900">{param.name}</span>
                                    <span className="text-xs px-2 py-1 bg-slate-200 text-slate-700 rounded">
                                      {param.type}
                                    </span>
                                    {param.required && (
                                      <span className="text-xs px-2 py-1 bg-red-100 text-red-700 rounded">
                                        Required
                                      </span>
                                    )}
                                  </div>
                                  {param.description && (
                                    <p className="text-sm text-slate-600 mt-1">{param.description}</p>
                                  )}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {endpoint.responses && endpoint.responses.length > 0 && (
                          <div>
                            <h4 className="font-semibold text-slate-900 mb-3">Responses</h4>
                            <div className="space-y-2">
                              {endpoint.responses.map((response, ridx) => (
                                <div key={ridx} className="p-3 bg-white rounded border border-slate-200">
                                  <div className="flex items-center gap-2">
                                    <span className={`font-semibold px-2 py-1 rounded text-white text-sm ${
                                      response.status_code < 300
                                        ? "bg-green-600"
                                        : response.status_code < 400
                                          ? "bg-blue-600"
                                          : response.status_code < 500
                                            ? "bg-yellow-600"
                                            : "bg-red-600"
                                    }`}>
                                      {response.status_code}
                                    </span>
                                    <span className="text-slate-700">{response.description}</span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {endpoint.security && endpoint.security.length > 0 && (
                          <div>
                            <h4 className="font-semibold text-slate-900 mb-2">Security</h4>
                            <div className="flex gap-2 flex-wrap">
                              {endpoint.security.map((sec, sidx) => (
                                <span key={sidx} className="px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm">
                                  {sec}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
