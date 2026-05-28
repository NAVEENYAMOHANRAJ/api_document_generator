"use client";

import { useState } from "react";
import { GitBranch, Loader, AlertCircle, ChevronDown, ChevronUp, Zap } from "lucide-react";

interface Endpoint {
  method: string;
  path: string;
  handler?: string;
  middleware: string[];
  source_file: string;
  line_number: number;
  confidence: number;
  summary: string;
  description: string;
}

interface Feature {
  name: string;
  value: string;
  confidence: number;
  score: number;
}

interface ExtractionResult {
  status: string;
  framework: string;
  total_endpoints: number;
  endpoints: Endpoint[];
  statistics: {
    total_endpoints: number;
    methods: Record<string, number>;
    files_scanned: number;
    average_confidence: number;
  };
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001/api";

const FEATURE_NAMES: Record<string, string> = {
  authentication: "🔐 Authentication",
  rate_limiting: "⚡ Rate Limiting",
  caching: "💾 Caching",
  pagination: "📄 Pagination",
  filtering: "🔍 Filtering",
  sorting: "↕️ Sorting",
  error_handling: "⚠️ Error Handling",
  input_validation: "✓ Input Validation",
  response_transformation: "🔄 Response Transform",
  versioning: "📦 Versioning",
  documentation: "📚 Documentation",
};

export default function LaravelDashboard() {
  const [repoUrl, setRepoUrl] = useState("https://github.com/gothinkster/laravel-realworld-example-app");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<ExtractionResult | null>(null);
  const [expandedEndpoint, setExpandedEndpoint] = useState<string | null>(null);
  const [endpointFeatures, setEndpointFeatures] = useState<Record<string, Record<string, Feature>>>({});
  const [loadingFeatures, setLoadingFeatures] = useState<Record<string, boolean>>({});

  const handleExtract = async () => {
    if (!repoUrl.trim()) {
      setError("Please enter a repository URL");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/extract-laravel`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repo_url: repoUrl.trim(),
          github_token: null,
        }),
      });

      if (!response.ok) {
        let errorMessage = "Extraction failed";
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
        } catch {
          errorMessage = response.statusText || `HTTP ${response.status}`;
        }

        if (response.status === 404) {
          throw new Error(`Repository not found. Check the URL: ${repoUrl}`);
        } else if (response.status === 401) {
          throw new Error("Authentication failed. Check your GitHub token.");
        } else if (response.status === 400) {
          throw new Error(`Invalid input: ${errorMessage}`);
        } else if (response.status === 422) {
          throw new Error(`Invalid repository: ${errorMessage}`);
        } else if (response.status === 504) {
          throw new Error(`Request timeout: ${errorMessage}`);
        } else if (response.status >= 500) {
          throw new Error(`Server error: ${errorMessage}`);
        } else {
          throw new Error(errorMessage);
        }
      }

      const data = await response.json();

      if (!data || typeof data !== "object") {
        throw new Error("Invalid response format from server");
      }

      if (data.status !== "success") {
        throw new Error(data.detail || "Extraction returned unsuccessful status");
      }

      if (!Array.isArray(data.endpoints)) {
        throw new Error("Invalid endpoints data in response");
      }

      if (data.endpoints.length === 0) {
        throw new Error("No endpoints found in the repository");
      }

      setResult(data);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "An unexpected error occurred";
      setError(errorMsg);
      console.error("Extraction error:", err);
    } finally {
      setLoading(false);
    }
  };

  const extractEndpointFeatures = async (endpoint: Endpoint, index: number) => {
    const endpointId = `${endpoint.method}-${endpoint.path}-${index}`;
    
    // Don't fetch if already loading or already have features
    if (loadingFeatures[endpointId] || endpointFeatures[endpointId]) {
      return;
    }

    setLoadingFeatures(prev => ({ ...prev, [endpointId]: true }));

    try {
      const endpointCode = `
// ${endpoint.method} ${endpoint.path}
// Handler: ${endpoint.handler || 'Closure'}
// Middleware: ${endpoint.middleware.join(', ') || 'None'}
// ${endpoint.description}
      `.trim();

      console.log("Fetching features for:", endpointId);

      const response = await fetch(`${API_BASE_URL}/extract-features`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: endpointCode,
          file_path: endpoint.source_file,
        }),
      });

      if (!response.ok) {
        console.error("Feature extraction failed:", response.status, response.statusText);
        setLoadingFeatures(prev => ({ ...prev, [endpointId]: false }));
        return;
      }

      const data = await response.json();
      console.log("Features received:", data);

      const features: Record<string, Feature> = {};
      
      if (data.features) {
        Object.entries(data.features).forEach(([key, value]: [string, any]) => {
          features[key] = {
            name: FEATURE_NAMES[key] || key.replace(/_/g, ' '),
            value: value.value || 'Not detected',
            confidence: value.confidence || 0,
            score: data.scores?.[key] || 0,
          };
        });
      }

      console.log("Processed features:", features);

      setEndpointFeatures(prev => ({
        ...prev,
        [endpointId]: features,
      }));
    } catch (err) {
      console.error("Feature extraction error:", err);
    } finally {
      setLoadingFeatures(prev => ({ ...prev, [endpointId]: false }));
    }
  };

  const handleExpandEndpoint = (endpointId: string, endpoint: Endpoint, index: number) => {
    const isCurrentlyExpanded = expandedEndpoint === endpointId;
    setExpandedEndpoint(isCurrentlyExpanded ? null : endpointId);

    // Fetch features when expanding
    if (!isCurrentlyExpanded) {
      extractEndpointFeatures(endpoint, index);
    }
  };

  const getMethodColor = (method: string) => {
    const colors: Record<string, string> = {
      GET: "bg-blue-100 text-blue-800",
      POST: "bg-green-100 text-green-800",
      PUT: "bg-yellow-100 text-yellow-800",
      DELETE: "bg-red-100 text-red-800",
      PATCH: "bg-purple-100 text-purple-800",
    };
    return colors[method] || "bg-gray-100 text-gray-800";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <div className="bg-slate-800 border-b border-slate-700 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex items-center gap-3 mb-2">
            <GitBranch className="text-blue-400" size={32} />
            <h1 className="text-4xl font-bold text-white">Laravel API Extractor</h1>
          </div>
          <p className="text-slate-400">Extract and analyze Laravel API endpoints from repositories</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Input Section */}
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-8 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6">Extract Endpoints</h2>

          {/* Repository URL Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-slate-300 mb-2">Repository URL</label>
            <input
              type="text"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/user/repo"
              className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            />
          </div>

          {/* Extract Button */}
          <button
            onClick={handleExtract}
            disabled={loading}
            className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white font-semibold rounded-lg flex items-center justify-center gap-2 transition-colors"
          >
            {loading ? (
              <>
                <Loader className="animate-spin" size={20} />
                Extracting...
              </>
            ) : (
              <>
                <GitBranch size={20} />
                Extract Endpoints
              </>
            )}
          </button>

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-900 border border-red-700 rounded-lg flex gap-3">
              <AlertCircle className="text-red-400 flex-shrink-0 mt-0.5" size={20} />
              <div className="flex-1">
                <p className="text-red-200 font-medium">Extraction Error</p>
                <p className="text-red-300 text-sm mt-1">{error}</p>
              </div>
            </div>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            {/* Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
                <p className="text-slate-400 text-sm font-medium">Total Endpoints</p>
                <p className="text-3xl font-bold text-white mt-2">{result.total_endpoints}</p>
              </div>
              <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
                <p className="text-slate-400 text-sm font-medium">Framework</p>
                <p className="text-3xl font-bold text-blue-400 mt-2 capitalize">{result.framework}</p>
              </div>
              <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
                <p className="text-slate-400 text-sm font-medium">Files Scanned</p>
                <p className="text-3xl font-bold text-white mt-2">{result.statistics.files_scanned}</p>
              </div>
              <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
                <p className="text-slate-400 text-sm font-medium">Avg Confidence</p>
                <p className="text-3xl font-bold text-green-400 mt-2">
                  {(result.statistics.average_confidence * 100).toFixed(0)}%
                </p>
              </div>
            </div>

            {/* HTTP Methods */}
            <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
              <h3 className="text-lg font-semibold text-white mb-4">HTTP Methods</h3>
              <div className="flex gap-4 flex-wrap">
                {Object.entries(result.statistics.methods).map(([method, count]) => (
                  <div key={method} className="flex items-center gap-2">
                    <span className={`px-3 py-1 rounded font-semibold text-sm ${getMethodColor(method)}`}>
                      {method}
                    </span>
                    <span className="text-slate-400 font-medium">{count}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Endpoints List */}
            <div>
              <h3 className="text-lg font-semibold text-white mb-4">Endpoints</h3>
              <div className="space-y-3">
                {result.endpoints.map((endpoint, idx) => {
                  const endpointId = `${endpoint.method}-${endpoint.path}-${idx}`;
                  const isExpanded = expandedEndpoint === endpointId;
                  const features = endpointFeatures[endpointId];
                  const isLoadingFeatures = loadingFeatures[endpointId];

                  return (
                    <div
                      key={idx}
                      className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden hover:border-slate-600 transition-colors"
                    >
                      <button
                        onClick={() => handleExpandEndpoint(endpointId, endpoint, idx)}
                        className="w-full p-4 flex items-center justify-between hover:bg-slate-700/50 transition-colors"
                      >
                        <div className="flex items-center gap-4 flex-1 text-left">
                          <span className={`px-3 py-1 rounded font-semibold text-sm ${getMethodColor(endpoint.method)}`}>
                            {endpoint.method}
                          </span>
                          <div className="flex-1">
                            <p className="font-mono font-semibold text-white">{endpoint.path}</p>
                            <p className="text-sm text-slate-400 mt-1">{endpoint.summary}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-xs text-slate-500">{endpoint.source_file}</p>
                            <p className="text-xs text-slate-500">Line {endpoint.line_number}</p>
                            <span className="inline-block mt-1 px-2 py-1 bg-blue-900 text-blue-300 rounded text-xs font-medium">
                              {(endpoint.confidence * 100).toFixed(0)}%
                            </span>
                          </div>
                        </div>
                        {isExpanded ? (
                          <ChevronUp className="text-slate-400 ml-4" size={20} />
                        ) : (
                          <ChevronDown className="text-slate-400 ml-4" size={20} />
                        )}
                      </button>

                      {isExpanded && (
                        <div className="border-t border-slate-700 p-4 bg-slate-700/30 space-y-4">
                          {endpoint.description && (
                            <div>
                              <h4 className="font-semibold text-slate-300 mb-2">Description</h4>
                              <p className="text-slate-400">{endpoint.description}</p>
                            </div>
                          )}

                          {endpoint.handler && (
                            <div>
                              <h4 className="font-semibold text-slate-300 mb-2">Handler</h4>
                              <p className="font-mono text-slate-300">{endpoint.handler}</p>
                            </div>
                          )}

                          {endpoint.middleware && endpoint.middleware.length > 0 && (
                            <div>
                              <h4 className="font-semibold text-slate-300 mb-2">Middleware</h4>
                              <div className="flex gap-2 flex-wrap">
                                {endpoint.middleware.map((mw, midx) => (
                                  <span key={midx} className="px-2 py-1 bg-slate-600 text-slate-300 rounded text-sm">
                                    {mw}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Features Section */}
                          <div className="border-t border-slate-600 pt-4">
                            <div className="flex items-center gap-2 mb-3">
                              <Zap className="text-yellow-400" size={18} />
                              <h4 className="font-semibold text-slate-300">API Features (11)</h4>
                            </div>

                            {isLoadingFeatures && !features ? (
                              <div className="flex items-center gap-2 text-slate-400">
                                <Loader className="animate-spin" size={16} />
                                <span className="text-sm">Analyzing features...</span>
                              </div>
                            ) : features && Object.keys(features).length > 0 ? (
                              <div className="grid grid-cols-2 gap-3">
                                {Object.entries(features).map(([key, feature]) => (
                                  <div key={key} className="bg-slate-700/50 rounded-lg p-3 border border-slate-600">
                                    <p className="text-xs font-semibold text-slate-200 mb-2">{feature.name}</p>
                                    <div className="flex items-center justify-between mb-2">
                                      <span className="text-xs text-slate-400 truncate">{feature.value}</span>
                                      <span className="text-xs font-bold text-blue-400 ml-2">{(feature.score * 100).toFixed(0)}%</span>
                                    </div>
                                    <div className="w-full bg-slate-600 rounded-full h-1.5">
                                      <div
                                        className="bg-gradient-to-r from-blue-500 to-cyan-400 h-1.5 rounded-full transition-all"
                                        style={{ width: `${Math.max(5, feature.score * 100)}%` }}
                                      />
                                    </div>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <div className="grid grid-cols-2 gap-3">
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">🔐 Authentication</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">⚡ Rate Limiting</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">💾 Caching</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">📄 Pagination</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">🔍 Filtering</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">↕️ Sorting</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">⚠️ Error Handling</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">✓ Input Validation</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">🔄 Response Transform</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">📦 Versioning</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                                <div className="bg-slate-700/50 rounded-lg p-3 border border-slate-600 opacity-50">
                                  <p className="text-xs font-semibold text-slate-200 mb-2">📚 Documentation</p>
                                  <p className="text-xs text-slate-500">Click to analyze...</p>
                                </div>
                              </div>
                            )}
                          </div>

                          <div className="pt-2 border-t border-slate-600">
                            <p className="text-xs text-slate-500">
                              Source: {endpoint.source_file}:{endpoint.line_number}
                            </p>
                            <p className="text-xs text-slate-500 mt-1">
                              Confidence: {(endpoint.confidence * 100).toFixed(0)}%
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!result && !loading && (
          <div className="text-center py-12">
            <GitBranch className="mx-auto text-slate-600 mb-4" size={48} />
            <p className="text-slate-400 text-lg">Enter a repository URL and click Extract to get started</p>
          </div>
        )}
      </div>
    </div>
  );
}
