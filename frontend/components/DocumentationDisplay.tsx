'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Copy, Download, Eye } from 'lucide-react';
import { InteractiveTestingPanel } from './InteractiveTestingPanel';

interface DocumentationDisplayProps {
  jobId: string;
  apiData: any;
}

export function DocumentationDisplay({ jobId, apiData }: DocumentationDisplayProps) {
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadMarkdown = () => {
    const element = document.createElement('a');
    const file = new Blob([generateMarkdown()], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = `api-documentation-${jobId}.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const generateMarkdown = () => {
    return `# API Documentation

## 1. Overview
${apiData.api?.description || 'API Description'}

**Base URL:** ${apiData.api?.baseUrl || 'https://api.example.com'}
**Version:** ${apiData.api?.version || 'v1'}
**Framework:** ${apiData.api?.framework || 'Unknown'}

## 2. Authentication
${apiData.authentication?.map((auth: any) => `- ${auth.type}: ${auth.scheme}`).join('\n') || 'No authentication methods'}

## 3. Endpoints
${apiData.endpoints?.map((ep: any) => `- ${ep.method} ${ep.path}`).join('\n') || 'No endpoints'}

## 4. Error Handling
${apiData.errorDefinitions?.map((err: any) => `- ${err.code}: ${err.message}`).join('\n') || 'No error definitions'}

## 5. Rate Limiting
Limit: ${apiData.rateLimits?.limit || 'N/A'}
Window: ${apiData.rateLimits?.window || 'N/A'}

## 6. Data Models
${Object.keys(apiData.schemas || {}).join(', ') || 'No schemas'}

## 7. Pagination
Supported on list endpoints

## 8. Webhooks
${apiData.webhooks?.length || 0} webhook events

## 9. Code Examples
See documentation for examples in Python, JavaScript, cURL, PHP, Go

## 10. Changelog
${apiData.changelog?.map((entry: any) => `- ${entry.version}: ${entry.changes?.join(', ')}`).join('\n') || 'No changelog'}
`;
  };

  return (
    <div className="w-full space-y-6">
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-11 gap-1">
          <TabsTrigger value="overview" className="text-xs">Overview</TabsTrigger>
          <TabsTrigger value="auth" className="text-xs">Auth</TabsTrigger>
          <TabsTrigger value="endpoints" className="text-xs">Endpoints</TabsTrigger>
          <TabsTrigger value="testing" className="text-xs">🧪 Try It</TabsTrigger>
          <TabsTrigger value="errors" className="text-xs">Errors</TabsTrigger>
          <TabsTrigger value="ratelimit" className="text-xs">Rate Limit</TabsTrigger>
          <TabsTrigger value="schemas" className="text-xs">Schemas</TabsTrigger>
          <TabsTrigger value="pagination" className="text-xs">Pagination</TabsTrigger>
          <TabsTrigger value="webhooks" className="text-xs">Webhooks</TabsTrigger>
          <TabsTrigger value="examples" className="text-xs">Examples</TabsTrigger>
          <TabsTrigger value="changelog" className="text-xs">Changelog</TabsTrigger>
        </TabsList>

        {/* 1. OVERVIEW */}
        <TabsContent value="overview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>1. Overview</CardTitle>
              <CardDescription>API metadata and versioning information</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-semibold">API Name</label>
                  <p className="text-lg">{apiData.api?.name || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold">Version</label>
                  <p className="text-lg">{apiData.api?.version || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold">Base URL</label>
                  <p className="text-sm font-mono">{apiData.api?.baseUrl || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold">Framework</label>
                  <p className="text-lg">{apiData.api?.framework || 'N/A'}</p>
                </div>
              </div>
              <div>
                <label className="text-sm font-semibold">Description</label>
                <p className="text-sm text-gray-600">{apiData.api?.description || 'N/A'}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-semibold">Contact</label>
                  <p className="text-sm">{apiData.api?.contact?.name || 'N/A'}</p>
                  <p className="text-xs text-gray-500">{apiData.api?.contact?.email || ''}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold">License</label>
                  <p className="text-sm">{apiData.api?.license?.name || 'N/A'}</p>
                </div>
              </div>
              <div>
                <label className="text-sm font-semibold">Versioning Strategy</label>
                <p className="text-sm">{apiData.versioning?.strategy || 'N/A'}</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 2. AUTHENTICATION */}
        <TabsContent value="auth" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>2. Authentication</CardTitle>
              <CardDescription>Authentication methods and credentials</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {apiData.authentication && apiData.authentication.length > 0 ? (
                apiData.authentication.map((auth: any, idx: number) => (
                  <div key={idx} className="border rounded-lg p-4 space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="font-semibold">{auth.type}</h4>
                      <Badge>{auth.scheme}</Badge>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>
                        <span className="font-semibold">Header:</span> {auth.header}
                      </div>
                      <div>
                        <span className="font-semibold">Format:</span> {auth.format}
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">{auth.description}</p>
                  </div>
                ))
              ) : (
                <p className="text-gray-500">No authentication methods found</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 3. ENDPOINTS */}
        <TabsContent value="endpoints" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>3. Endpoints</CardTitle>
              <CardDescription>API endpoints with methods and paths</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {apiData.endpoints && apiData.endpoints.length > 0 ? (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {apiData.endpoints.map((endpoint: any, idx: number) => (
                    <div key={idx} className="border rounded-lg p-3 space-y-2">
                      <div className="flex items-center gap-2">
                        <Badge className="bg-blue-600">{endpoint.method}</Badge>
                        <code className="text-sm font-mono">{endpoint.path}</code>
                      </div>
                      <p className="text-sm">{endpoint.summary || endpoint.description}</p>
                      {endpoint.middleware && endpoint.middleware.length > 0 && (
                        <div className="text-xs">
                          <span className="font-semibold">Middleware:</span> {endpoint.middleware.join(', ')}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No endpoints found</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* INTERACTIVE TESTING */}
        <TabsContent value="testing" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>🧪 Try It Out - Interactive Testing</CardTitle>
              <CardDescription>Test endpoints directly from documentation</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.endpoints && apiData.endpoints.length > 0 ? (
                <div className="space-y-6">
                  {apiData.endpoints.map((endpoint: any, idx: number) => (
                    <div key={idx} className="border rounded-lg p-4 space-y-4">
                      <div className="flex items-center gap-2 mb-4">
                        <Badge className="bg-blue-600">{endpoint.method}</Badge>
                        <code className="text-sm font-mono">{endpoint.path}</code>
                      </div>
                      <InteractiveTestingPanel 
                        endpoint={endpoint}
                        baseUrl={apiData.api?.baseUrl || 'http://localhost:8000'}
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No endpoints available for testing</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 4. ERROR HANDLING */}
        <TabsContent value="errors" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>4. Error Handling</CardTitle>
              <CardDescription>Error codes and response formats</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.errorDefinitions && apiData.errorDefinitions.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="border-b">
                      <tr>
                        <th className="text-left py-2">Code</th>
                        <th className="text-left py-2">Status</th>
                        <th className="text-left py-2">Message</th>
                      </tr>
                    </thead>
                    <tbody>
                      {apiData.errorDefinitions.map((err: any, idx: number) => (
                        <tr key={idx} className="border-b">
                          <td className="py-2 font-mono text-xs">{err.code}</td>
                          <td className="py-2">{err.status_code}</td>
                          <td className="py-2">{err.message}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-gray-500">No error definitions found</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 5. RATE LIMITING */}
        <TabsContent value="ratelimit" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>5. Rate Limiting</CardTitle>
              <CardDescription>Rate limit policy and headers</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {apiData.rateLimits ? (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="border rounded-lg p-3">
                      <label className="text-sm font-semibold">Limit</label>
                      <p className="text-2xl font-bold">{apiData.rateLimits.limit}</p>
                    </div>
                    <div className="border rounded-lg p-3">
                      <label className="text-sm font-semibold">Window</label>
                      <p className="text-lg">{apiData.rateLimits.window}</p>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-sm font-semibold mb-2">Response Headers:</p>
                    <code className="text-xs">X-RateLimit-Limit: {apiData.rateLimits.limit}</code><br/>
                    <code className="text-xs">X-RateLimit-Remaining: [remaining]</code><br/>
                    <code className="text-xs">X-RateLimit-Reset: [timestamp]</code>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500">No rate limiting information</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 6. DATA MODELS */}
        <TabsContent value="schemas" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>6. Data Models / Schemas</CardTitle>
              <CardDescription>Reusable object definitions</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.schemas && Object.keys(apiData.schemas).length > 0 ? (
                <div className="space-y-4">
                  {Object.entries(apiData.schemas).map(([name, schema]: [string, any]) => (
                    <div key={name} className="border rounded-lg p-3">
                      <h4 className="font-semibold mb-2">{name}</h4>
                      <pre className="bg-gray-50 p-2 rounded text-xs overflow-x-auto">
                        {JSON.stringify(schema, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No schemas found</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 7. PAGINATION */}
        <TabsContent value="pagination" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>7. Pagination</CardTitle>
              <CardDescription>Pagination parameters and response format</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div>
                  <h4 className="font-semibold mb-2">Query Parameters</h4>
                  <table className="w-full text-sm">
                    <thead className="border-b">
                      <tr>
                        <th className="text-left py-2">Parameter</th>
                        <th className="text-left py-2">Type</th>
                        <th className="text-left py-2">Default</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="border-b">
                        <td className="py-2">page</td>
                        <td>integer</td>
                        <td>1</td>
                      </tr>
                      <tr className="border-b">
                        <td className="py-2">limit</td>
                        <td>integer</td>
                        <td>20</td>
                      </tr>
                      <tr>
                        <td className="py-2">sort</td>
                        <td>string</td>
                        <td>-</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Response Format</h4>
                  <pre className="bg-gray-50 p-3 rounded text-xs overflow-x-auto">
{`{
  "data": [...],
  "pagination": {
    "total": 200,
    "page": 1,
    "limit": 20,
    "total_pages": 10,
    "next": "/api/resource?page=2",
    "prev": null
  }
}`}
                  </pre>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 8. WEBHOOKS */}
        <TabsContent value="webhooks" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>8. Webhooks</CardTitle>
              <CardDescription>Webhook events and payloads</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.webhooks && apiData.webhooks.length > 0 ? (
                <div className="space-y-3">
                  {apiData.webhooks.map((webhook: any, idx: number) => (
                    <div key={idx} className="border rounded-lg p-3">
                      <h4 className="font-semibold">{webhook.event}</h4>
                      <pre className="bg-gray-50 p-2 rounded text-xs mt-2 overflow-x-auto">
                        {JSON.stringify(webhook.payload, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No webhooks defined</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 9. CODE EXAMPLES */}
        <TabsContent value="examples" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>9. Code Examples</CardTitle>
              <CardDescription>Working examples in multiple languages</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold mb-2">Python</h4>
                  <pre className="bg-gray-50 p-3 rounded text-xs overflow-x-auto">
{`import requests
headers = {"Authorization": "Bearer <token>"}
response = requests.get("${apiData.api?.baseUrl}/users", headers=headers)
print(response.json())`}
                  </pre>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">JavaScript</h4>
                  <pre className="bg-gray-50 p-3 rounded text-xs overflow-x-auto">
{`const response = await fetch("${apiData.api?.baseUrl}/users", {
  headers: { "Authorization": "Bearer <token>" }
});
const data = await response.json();
console.log(data);`}
                  </pre>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">cURL</h4>
                  <pre className="bg-gray-50 p-3 rounded text-xs overflow-x-auto">
{`curl -X GET "${apiData.api?.baseUrl}/users" \\
  -H "Authorization: Bearer <token>"`}
                  </pre>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 10. CHANGELOG */}
        <TabsContent value="changelog" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>10. Changelog & Versioning</CardTitle>
              <CardDescription>Version history and changes</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.changelog && apiData.changelog.length > 0 ? (
                <div className="space-y-3">
                  {apiData.changelog.map((entry: any, idx: number) => (
                    <div key={idx} className="border rounded-lg p-3">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold">{entry.version}</h4>
                        <span className="text-xs text-gray-500">{entry.date}</span>
                      </div>
                      <ul className="text-sm space-y-1">
                        {entry.changes?.map((change: string, cidx: number) => (
                          <li key={cidx} className="text-gray-600">• {change}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No changelog available</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Export Options */}
      <Card>
        <CardHeader>
          <CardTitle>Export Documentation</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-2">
          <Button onClick={downloadMarkdown} className="gap-2">
            <Download className="w-4 h-4" />
            Download Markdown
          </Button>
          <Button onClick={() => copyToClipboard(generateMarkdown())} variant="outline" className="gap-2">
            <Copy className="w-4 h-4" />
            {copied ? 'Copied!' : 'Copy Markdown'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
