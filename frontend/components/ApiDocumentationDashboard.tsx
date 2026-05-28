"use client";

import { useState } from "react";
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
} from "lucide-react";

interface ApiDocumentation {
  overview: {
    name: string;
    version: string;
    baseUrl: string;
    description: string;
  };
  authentication: {
    methods: Array<{
      type: string;
      description: string;
      example?: string;
    }>;
  };
  endpoints: Array<{
    method: string;
    path: string;
    summary: string;
    description: string;
    parameters?: Array<{
      name: string;
      type: string;
      required: boolean;
      description: string;
    }>;
    requestBody?: {
      type: string;
      example: any;
    };
    responses: Array<{
      status: number;
      description: string;
      schema?: any;
    }>;
  }>;
  rateLimit?: {
    requestsPerMinute: number;
    requestsPerHour: number;
    headers: string[];
  };
  schemas: Record<string, any>;
  pagination?: {
    style: string;
    parameters: string[];
    example: string;
  };
  webhooks?: Array<{
    event: string;
    description: string;
    payload: any;
  }>;
  errors: Array<{
    code: number;
    message: string;
    description: string;
  }>;
  changelog?: Array<{
    version: string;
    date: string;
    changes: string[];
  }>;
}

interface DashboardProps {
  documentation: ApiDocumentation;
}

export default function ApiDocumentationDashboard({
  documentation,
}: DashboardProps) {
  const [activeTab, setActiveTab] = useState("overview");
  const [expandedEndpoint, setExpandedEndpoint] = useState<string | null>(null);
  const [copiedCode, setCopiedCode] = useState<string | null>(null);

  const tabs = [
    { id: "overview", label: "Overview", icon: FileText },
    { id: "authentication", label: "Authentication", icon: Lock },
    { id: "endpoints", label: "Endpoints", icon: Globe },
    { id: "try-it", label: "Try It", icon: Zap },
    { id: "errors", label: "Errors", icon: AlertCircle },
    { id: "rate-limit", label: "Rate Limit", icon: Code },
    { id: "schemas", label: "Schemas", icon: BookOpen },
    { id: "pagination", label: "Pagination", icon: ChevronDown },
    { id: "webhooks", label: "Webhooks", icon: Webhook },
    { id: "changelog", label: "Changelog", icon: FileText },
  ];

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-4xl font-bold text-slate-900">
                {documentation.overview.name}
              </h1>
              <p className="text-slate-600 mt-2">
                {documentation.overview.description}
              </p>
              <div className="flex gap-4 mt-4 text-sm">
                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full font-medium">
                  v{documentation.overview.version}
                </span>
                <span className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full font-mono">
                  {documentation.overview.baseUrl}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="border-t border-slate-200 overflow-x-auto">
          <div className="max-w-7xl mx-auto px-6 flex gap-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-3 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap ${
                    activeTab === tab.id
                      ? "border-blue-600 text-blue-600"
                      : "border-transparent text-slate-600 hover:text-slate-900"
                  }`}
                >
                  <Icon size={16} />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Overview Tab */}
        {activeTab === "overview" && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg border border-slate-200 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-4">
                API Overview
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="p-4 bg-slate-50 rounded-lg">
                  <p className="text-sm text-slate-600 font-medium">API Name</p>
                  <p className="text-lg font-semibold text-slate-900 mt-1">
                    {documentation.overview.name}
                  </p>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <p className="text-sm text-slate-600 font-medium">Version</p>
                  <p className="text-lg font-semibold text-slate-900 mt-1">
                    {documentation.overview.version}
                  </p>
                </div>
                <div className="p-4 bg-slate-50 rounded-lg">
                  <p className="text-sm text-slate-600 font-medium">Base URL</p>
                  <p className="text-lg font-mono font-semibold text-slate-900 mt-1">
                    {documentation.overview.baseUrl}
                  </p>
                </div>
              </div>
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-slate-700">{documentation.overview.description}</p>
              </div>
            </div>
          </div>
        )}

        {/* Authentication Tab */}
        {activeTab === "authentication" && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg border border-slate-200 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">
                Authentication Methods
              </h2>
              <div className="space-y-6">
                {documentation.authentication.methods.map((method, idx) => (
                  <div
                    key={idx}
                    className="p-6 border border-slate-200 rounded-lg hover:border-blue-300 transition-colors"
                  >
                    <h3 className="text-lg font-semibold text-slate-900 mb-2">
                      {method.type}
                    </h3>
                    <p className="text-slate-600 mb-4">{method.description}</p>
                    {method.example && (
                      <div className="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                        <pre>{method.example}</pre>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Endpoints Tab */}
        {activeTab === "endpoints" && (
          <div className="space-y-4">
            <div className="bg-white rounded-lg border border-slate-200 p-8 mb-6">
              <h2 className="text-2xl font-bold text-slate-900 mb-2">
                API Endpoints
              </h2>
              <p className="text-slate-600">
                Total endpoints: {documentation.endpoints.length}
              </p>
            </div>
            {documentation.endpoints.map((endpoint, idx) => {
              const endpointId = `${endpoint.method}-${endpoint.path}`;
              const isExpanded = expandedEndpoint === endpointId;
              return (
                <div
                  key={idx}
                  className="bg-white rounded-lg border border-slate-200 overflow-hidden hover:border-blue-300 transition-colors"
                >
                  <button
                    onClick={() =>
                      setExpandedEndpoint(isExpanded ? null : endpointId)
                    }
                    className="w-full p-6 flex items-center justify-between hover:bg-slate-50 transition-colors"
                  >
                    <div className="flex items-center gap-4 flex-1 text-left">
                      <span
                        className={`px-3 py-1 rounded font-semibold text-white text-sm ${
                          endpoint.method === "GET"
                            ? "bg-blue-600"
                            : endpoint.method === "POST"
                              ? "bg-green-600"
                              : endpoint.method === "PUT"
                                ? "bg-yellow-600"
                                : endpoint.method === "DELETE"
                                  ? "bg-red-600"
                                  : "bg-slate-600"
                        }`}
                      >
                        {endpoint.method}
                      </span>
                      <div className="flex-1">
                        <p className="font-mono font-semibold text-slate-900">
                          {endpoint.path}
                        </p>
                        <p className="text-sm text-slate-600 mt-1">
                          {endpoint.summary}
                        </p>
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
                          <h4 className="font-semibold text-slate-900 mb-2">
                            Description
                          </h4>
                          <p className="text-slate-700">{endpoint.description}</p>
                        </div>
                      )}

                      {endpoint.parameters && endpoint.parameters.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-slate-900 mb-3">
                            Parameters
                          </h4>
                          <div className="space-y-2">
                            {endpoint.parameters.map((param, pidx) => (
                              <div
                                key={pidx}
                                className="p-3 bg-white rounded border border-slate-200"
                              >
                                <div className="flex items-center gap-2">
                                  <span className="font-mono font-semibold text-slate-900">
                                    {param.name}
                                  </span>
                                  <span className="text-xs px-2 py-1 bg-slate-200 text-slate-700 rounded">
                                    {param.type}
                                  </span>
                                  {param.required && (
                                    <span className="text-xs px-2 py-1 bg-red-100 text-red-700 rounded">
                                      Required
                                    </span>
                                  )}
                                </div>
                                <p className="text-sm text-slate-600 mt-1">
                                  {param.description}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {endpoint.requestBody && (
                        <div>
                          <h4 className="font-semibold text-slate-900 mb-2">
                            Request Body
                          </h4>
                          <div className="bg-white p-4 rounded border border-slate-200 font-mono text-sm overflow-x-auto">
                            <pre className="text-slate-700">
                              {JSON.stringify(endpoint.requestBody.example, null, 2)}
                            </pre>
                          </div>
                        </div>
                      )}

                      {endpoint.responses && endpoint.responses.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-slate-900 mb-3">
                            Responses
                          </h4>
                          <div className="space-y-2">
                            {endpoint.responses.map((response, ridx) => (
                              <div
                                key={ridx}
                                className="p-3 bg-white rounded border border-slate-200"
                              >
                                <div className="flex items-center gap-2">
                                  <span
                                    className={`font-semibold px-2 py-1 rounded text-white text-sm ${
                                      response.status < 300
                                        ? "bg-green-600"
                                        : response.status < 400
                                          ? "bg-blue-600"
                                          : response.status < 500
                                            ? "bg-yellow-600"
                                            : "bg-red-600"
                                    }`}
                                  >
                                    {response.status}
                                  </span>
                                  <span className="text-slate-700">
                                    {response.description}
                                  </span>
                                </div>
                              </div>
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
        )}

        {/* Try It Tab */}
        {activeTab === "try-it" && (
          <div className="bg-white rounded-lg border border-slate-200 p-8">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">
              Interactive Testing
            </h2>
            <div className="p-6 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-slate-700">
                Select an endpoint from the Endpoints tab to test it interactively.
              </p>
            </div>
          </div>
        )}

        {/* Errors Tab */}
        {activeTab === "errors" && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg border border-slate-200 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">
                Error Codes
              </h2>
              <div className="space-y-3">
                {documentation.errors.map((error, idx) => (
                  <div
                    key={idx}
                    className="p-4 border border-slate-200 rounded-lg hover:border-red-300 transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <span className="px-3 py-1 bg-red-100 text-red-700 rounded font-semibold text-sm">
                        {error.code}
                      </span>
                      <div className="flex-1">
                        <p className="font-semibold text-slate-900">
                          {error.message}
                        </p>
                        <p className="text-sm text-slate-600 mt-1">
                          {error.description}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Rate Limit Tab */}
        {activeTab === "rate-limit" && documentation.rateLimit && (
          <div className="bg-white rounded-lg border border-slate-200 p-8">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">
              Rate Limiting
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div className="p-6 bg-slate-50 rounded-lg border border-slate-200">
                <p className="text-sm text-slate-600 font-medium">
                  Requests per Minute
                </p>
                <p className="text-3xl font-bold text-slate-900 mt-2">
                  {documentation.rateLimit.requestsPerMinute}
                </p>
              </div>
              <div className="p-6 bg-slate-50 rounded-lg border border-slate-200">
                <p className="text-sm text-slate-600 font-medium">
                  Requests per Hour
                </p>
                <p className="text-3xl font-bold text-slate-900 mt-2">
                  {documentation.rateLimit.requestsPerHour}
                </p>
              </div>
            </div>
            <div>
              <h3 className="font-semibold text-slate-900 mb-3">
                Rate Limit Headers
              </h3>
              <div className="space-y-2">
                {documentation.rateLimit.headers.map((header, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-slate-50 rounded border border-slate-200 font-mono text-sm"
                  >
                    {header}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Schemas Tab */}
        {activeTab === "schemas" && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg border border-slate-200 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">
                Data Schemas
              </h2>
              <div className="space-y-6">
                {Object.entries(documentation.schemas).map(([name, schema]) => (
                  <div
                    key={name}
                    className="p-6 border border-slate-200 rounded-lg"
                  >
                    <h3 className="font-semibold text-slate-900 mb-3">{name}</h3>
                    <div className="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                      <pre>{JSON.stringify(schema, null, 2)}</pre>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Pagination Tab */}
        {activeTab === "pagination" && documentation.pagination && (
          <div className="bg-white rounded-lg border border-slate-200 p-8">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">
              Pagination
            </h2>
            <div className="space-y-6">
              <div>
                <h3 className="font-semibold text-slate-900 mb-2">Style</h3>
                <p className="text-slate-700">{documentation.pagination.style}</p>
              </div>
              <div>
                <h3 className="font-semibold text-slate-900 mb-3">Parameters</h3>
                <div className="space-y-2">
                  {documentation.pagination.parameters.map((param, idx) => (
                    <div
                      key={idx}
                      className="p-3 bg-slate-50 rounded border border-slate-200 font-mono text-sm"
                    >
                      {param}
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="font-semibold text-slate-900 mb-2">Example</h3>
                <div className="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                  <pre>{documentation.pagination.example}</pre>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Webhooks Tab */}
        {activeTab === "webhooks" && documentation.webhooks && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg border border-slate-200 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">
                Webhooks
              </h2>
              <div className="space-y-6">
                {documentation.webhooks.map((webhook, idx) => (
                  <div
                    key={idx}
                    className="p-6 border border-slate-200 rounded-lg"
                  >
                    <h3 className="font-semibold text-slate-900 mb-2">
                      {webhook.event}
                    </h3>
                    <p className="text-slate-600 mb-4">{webhook.description}</p>
                    <div className="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                      <pre>{JSON.stringify(webhook.payload, null, 2)}</pre>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Changelog Tab */}
        {activeTab === "changelog" && documentation.changelog && (
          <div className="bg-white rounded-lg border border-slate-200 p-8">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">
              Changelog
            </h2>
            <div className="space-y-6">
              {documentation.changelog.map((entry, idx) => (
                <div key={idx} className="pb-6 border-b border-slate-200 last:border-b-0">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full font-semibold text-sm">
                      v{entry.version}
                    </span>
                    <span className="text-sm text-slate-600">{entry.date}</span>
                  </div>
                  <ul className="space-y-2">
                    {entry.changes.map((change, cidx) => (
                      <li key={cidx} className="text-slate-700 flex gap-2">
                        <span className="text-blue-600 font-bold">•</span>
                        {change}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
