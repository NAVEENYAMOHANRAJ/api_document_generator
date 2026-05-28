'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';

interface SimpleDocumentationDisplayProps {
  jobId: string;
  apiData: any;
}

export function SimpleDocumentationDisplay({ jobId, apiData }: SimpleDocumentationDisplayProps) {
  const [activeTab, setActiveTab] = useState('overview');

  if (!apiData) {
    return <div className="text-gray-500">No data available</div>;
  }

  return (
    <div className="w-full space-y-6">
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-11 gap-1 bg-slate-700">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="auth">Auth</TabsTrigger>
          <TabsTrigger value="endpoints">Endpoints</TabsTrigger>
          <TabsTrigger value="testing">Try It</TabsTrigger>
          <TabsTrigger value="errors">Errors</TabsTrigger>
          <TabsTrigger value="ratelimit">Rate Limit</TabsTrigger>
          <TabsTrigger value="schemas">Schemas</TabsTrigger>
          <TabsTrigger value="pagination">Pagination</TabsTrigger>
          <TabsTrigger value="webhooks">Webhooks</TabsTrigger>
          <TabsTrigger value="examples">Examples</TabsTrigger>
          <TabsTrigger value="changelog">Changelog</TabsTrigger>
        </TabsList>

        {/* 1. OVERVIEW */}
        <TabsContent value="overview">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">1. Overview</CardTitle>
              <CardDescription>API metadata and versioning</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-semibold">API Name</label>
                  <p className="text-lg text-white">{apiData.api?.name || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold">Version</label>
                  <p className="text-lg text-white">{apiData.api?.version || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold">Base URL</label>
                  <p className="text-sm font-mono text-blue-400">{apiData.api?.baseUrl || 'N/A'}</p>
                </div>
                <div>
                  <label className="text-sm font-semibold">Framework</label>
                  <p className="text-lg text-white">{apiData.api?.framework || 'N/A'}</p>
                </div>
              </div>
              <div>
                <label className="text-sm font-semibold">Description</label>
                <p className="text-sm">{apiData.api?.description || 'N/A'}</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 2. AUTHENTICATION */}
        <TabsContent value="auth">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">2. Authentication</CardTitle>
              <CardDescription>Authentication methods</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {apiData.authentication && apiData.authentication.length > 0 ? (
                apiData.authentication.map((auth: any, idx: number) => (
                  <div key={idx} className="border border-slate-600 rounded-lg p-4 space-y-2">
                    <div className="flex items-center gap-2">
                      <h4 className="font-semibold text-white">{auth.type}</h4>
                      <Badge>{auth.scheme}</Badge>
                    </div>
                    <p className="text-sm text-slate-400">Header: {auth.header}</p>
                    <p className="text-sm text-slate-400">Format: {auth.format}</p>
                  </div>
                ))
              ) : (
                <p className="text-slate-400">No authentication methods</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 3. ENDPOINTS */}
        <TabsContent value="endpoints">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">3. Endpoints</CardTitle>
              <CardDescription>API endpoints</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.endpoints && apiData.endpoints.length > 0 ? (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {apiData.endpoints.map((ep: any, idx: number) => (
                    <div key={idx} className="border border-slate-600 rounded-lg p-3">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge className="bg-blue-600">{ep.method}</Badge>
                        <code className="text-sm font-mono text-blue-400">{ep.path}</code>
                      </div>
                      <p className="text-sm text-slate-300">{ep.summary || ep.description}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-slate-400">No endpoints found</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 4. TRY IT OUT */}
        <TabsContent value="testing">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">🧪 Try It Out</CardTitle>
              <CardDescription>Interactive API testing</CardDescription>
            </CardHeader>
            <CardContent className="text-slate-300">
              <p>Select an endpoint above to test it interactively.</p>
              <p className="text-sm text-slate-400 mt-2">Features:</p>
              <ul className="text-sm text-slate-400 list-disc list-inside mt-2 space-y-1">
                <li>Environment selection (Local/Staging/Prod)</li>
                <li>Authentication token support</li>
                <li>Query parameters</li>
                <li>Request body editor</li>
                <li>Live response display</li>
                <li>cURL command generation</li>
              </ul>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 5. ERROR HANDLING */}
        <TabsContent value="errors">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">4. Error Handling</CardTitle>
              <CardDescription>Error codes and responses</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.errorDefinitions && apiData.errorDefinitions.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm text-slate-300">
                    <thead className="border-b border-slate-600">
                      <tr>
                        <th className="text-left py-2">Code</th>
                        <th className="text-left py-2">Status</th>
                        <th className="text-left py-2">Message</th>
                      </tr>
                    </thead>
                    <tbody>
                      {apiData.errorDefinitions.map((err: any, idx: number) => (
                        <tr key={idx} className="border-b border-slate-700">
                          <td className="py-2 font-mono text-xs">{err.code}</td>
                          <td className="py-2">{err.status_code}</td>
                          <td className="py-2">{err.message}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-slate-400">No error definitions</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 6. RATE LIMITING */}
        <TabsContent value="ratelimit">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">5. Rate Limiting</CardTitle>
              <CardDescription>Rate limit policy</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {apiData.rateLimits && Object.keys(apiData.rateLimits).length > 0 ? (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="border border-slate-600 rounded-lg p-3">
                      <label className="text-sm font-semibold text-slate-300">Limit</label>
                      <p className="text-2xl font-bold text-white">{apiData.rateLimits.limit}</p>
                    </div>
                    <div className="border border-slate-600 rounded-lg p-3">
                      <label className="text-sm font-semibold text-slate-300">Window</label>
                      <p className="text-lg text-white">{apiData.rateLimits.window}</p>
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-slate-400">No rate limiting information</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 7. DATA MODELS */}
        <TabsContent value="schemas">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">6. Data Models</CardTitle>
              <CardDescription>Reusable schemas</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.schemas && Object.keys(apiData.schemas).length > 0 ? (
                <div className="space-y-4">
                  {Object.entries(apiData.schemas).map(([name, schema]: [string, any]) => (
                    <div key={name} className="border border-slate-600 rounded-lg p-3">
                      <h4 className="font-semibold text-white mb-2">{name}</h4>
                      <pre className="bg-slate-700 p-2 rounded text-xs text-slate-300 overflow-x-auto">
                        {JSON.stringify(schema, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-slate-400">No schemas defined</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 8. PAGINATION */}
        <TabsContent value="pagination">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">7. Pagination</CardTitle>
              <CardDescription>Pagination parameters</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <div>
                <h4 className="font-semibold mb-2">Query Parameters</h4>
                <table className="w-full text-sm">
                  <thead className="border-b border-slate-600">
                    <tr>
                      <th className="text-left py-2">Parameter</th>
                      <th className="text-left py-2">Type</th>
                      <th className="text-left py-2">Default</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-b border-slate-700">
                      <td className="py-2">page</td>
                      <td>integer</td>
                      <td>1</td>
                    </tr>
                    <tr className="border-b border-slate-700">
                      <td className="py-2">limit</td>
                      <td>integer</td>
                      <td>20</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 9. WEBHOOKS */}
        <TabsContent value="webhooks">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">8. Webhooks</CardTitle>
              <CardDescription>Webhook events</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.webhooks && apiData.webhooks.length > 0 ? (
                <div className="space-y-3">
                  {apiData.webhooks.map((webhook: any, idx: number) => (
                    <div key={idx} className="border border-slate-600 rounded-lg p-3">
                      <h4 className="font-semibold text-white">{webhook.event}</h4>
                      <pre className="bg-slate-700 p-2 rounded text-xs text-slate-300 mt-2 overflow-x-auto">
                        {JSON.stringify(webhook.payload, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-slate-400">No webhooks defined</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 10. CODE EXAMPLES */}
        <TabsContent value="examples">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">9. Code Examples</CardTitle>
              <CardDescription>Working examples</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold text-white mb-2">Python</h4>
                <pre className="bg-slate-700 p-3 rounded text-xs text-slate-300 overflow-x-auto">
{`import requests
headers = {"Authorization": "Bearer <token>"}
response = requests.get("${apiData.api?.baseUrl}/users", headers=headers)
print(response.json())`}
                </pre>
              </div>
              <div>
                <h4 className="font-semibold text-white mb-2">JavaScript</h4>
                <pre className="bg-slate-700 p-3 rounded text-xs text-slate-300 overflow-x-auto">
{`const response = await fetch("${apiData.api?.baseUrl}/users", {
  headers: { "Authorization": "Bearer <token>" }
});
const data = await response.json();
console.log(data);`}
                </pre>
              </div>
              <div>
                <h4 className="font-semibold text-white mb-2">cURL</h4>
                <pre className="bg-slate-700 p-3 rounded text-xs text-slate-300 overflow-x-auto">
{`curl -X GET "${apiData.api?.baseUrl}/users" \\
  -H "Authorization: Bearer <token>"`}
                </pre>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 11. CHANGELOG */}
        <TabsContent value="changelog">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">10. Changelog</CardTitle>
              <CardDescription>Version history</CardDescription>
            </CardHeader>
            <CardContent>
              {apiData.changelog && apiData.changelog.length > 0 ? (
                <div className="space-y-3">
                  {apiData.changelog.map((entry: any, idx: number) => (
                    <div key={idx} className="border border-slate-600 rounded-lg p-3">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold text-white">{entry.version}</h4>
                        <span className="text-xs text-slate-400">{entry.date}</span>
                      </div>
                      <ul className="text-sm text-slate-300 space-y-1">
                        {entry.changes?.map((change: string, cidx: number) => (
                          <li key={cidx} className="text-slate-400">• {change}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-slate-400">No changelog available</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
