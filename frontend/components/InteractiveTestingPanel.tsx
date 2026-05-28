'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Loader2, Send, Copy, CheckCircle, AlertCircle } from 'lucide-react';

interface InteractiveTestingPanelProps {
  endpoint: any;
  baseUrl?: string;
}

export function InteractiveTestingPanel({ endpoint, baseUrl = 'http://localhost:8000' }: InteractiveTestingPanelProps) {
  const [environment, setEnvironment] = useState('local');
  const [authToken, setAuthToken] = useState('');
  const [queryParams, setQueryParams] = useState<Record<string, string>>({});
  const [requestBody, setRequestBody] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(false);
  const [testId, setTestId] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<any>(null);
  const [copied, setCopied] = useState(false);
  const [environments, setEnvironments] = useState<any[]>([]);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api';

  // Fetch environments
  useEffect(() => {
    const fetchEnvironments = async () => {
      try {
        const response = await fetch(`${API_BASE}/testing/environments`);
        if (!response.ok) {
          setEnvironments([]);
          return;
        }
        const data = await response.json();
        setEnvironments(Array.isArray(data?.environments) ? data.environments : []);
      } catch (error) {
        console.error('Failed to fetch environments:', error);
        setEnvironments([]);
      }
    };
    fetchEnvironments();
  }, [API_BASE]);

  // Initialize request body from schema
  useEffect(() => {
    if (endpoint.requestBody?.schema) {
      const initialBody: Record<string, any> = {};
      Object.keys(endpoint.requestBody.schema).forEach(key => {
        initialBody[key] = '';
      });
      setRequestBody(initialBody);
    }
  }, [endpoint]);

  // Poll for test results
  useEffect(() => {
    if (!testId) return;

    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE}/testing/test/${testId}`);
        const data = await response.json();

        if (data.status === 'completed' || data.status === 'failed') {
          setTestResult(data);
          setLoading(false);
          clearInterval(interval);
        }
      } catch (error) {
        console.error('Failed to fetch test result:', error);
      }
    }, 500);

    return () => clearInterval(interval);
  }, [testId, API_BASE]);

  const handleSendRequest = async () => {
    setLoading(true);
    setTestResult(null);

    try {
      const currentEnv = environments.find(e => e.name.toLowerCase() === environment);
      const baseUrlForTest = currentEnv?.base_url || baseUrl;

      const response = await fetch(`${API_BASE}/testing/test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          endpoint_method: endpoint.method,
          endpoint_path: endpoint.path,
          base_url: baseUrlForTest,
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          query_params: queryParams,
          request_body: endpoint.method !== 'GET' ? requestBody : undefined,
          auth_token: authToken
        })
      });

      const data = await response.json();
      setTestId(data.test_id);
    } catch (error) {
      setTestResult({
        status: 'failed',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const generateCurl = () => {
    const currentEnv = environments.find(e => e.name.toLowerCase() === environment);
    const baseUrlForCurl = currentEnv?.base_url || baseUrl;
    const url = `${baseUrlForCurl}${endpoint.path}`;

    let curl = `curl -X ${endpoint.method} "${url}"`;
    curl += ' \\\n  -H "Content-Type: application/json"';
    curl += ' \\\n  -H "Accept: application/json"';

    if (authToken) {
      curl += ` \\\n  -H "Authorization: Bearer ${authToken}"`;
    }

    if (endpoint.method !== 'GET' && Object.keys(requestBody).length > 0) {
      curl += ` \\\n  -d '${JSON.stringify(requestBody)}'`;
    }

    return curl;
  };

  return (
    <div className="w-full space-y-6">
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">🧪 Try It Out - Interactive Testing</CardTitle>
          <CardDescription>Test this endpoint directly from the documentation</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Environment Selection */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">Environment</label>
            <select
              value={environment}
              onChange={(e) => setEnvironment(e.target.value)}
              className="w-full px-3 py-2 bg-slate-700 border border-slate-600 text-white rounded-md"
            >
              <option value="local">Local - {baseUrl}</option>
              {environments.map((env) => (
                <option key={env.name} value={env.name.toLowerCase()}>
                  {env.name} - {env.base_url}
                </option>
              ))}
            </select>
          </div>

          {/* Authentication Token */}
          {endpoint.security && endpoint.security.length > 0 && (
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-2">
                Authorization Token
              </label>
              <Input
                type="password"
                placeholder="Enter your Bearer token"
                value={authToken}
                onChange={(e) => setAuthToken(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white"
              />
              <p className="text-xs text-slate-400 mt-1">
                This endpoint requires authentication
              </p>
            </div>
          )}

          {/* Query Parameters */}
          {endpoint.queryParameters && endpoint.queryParameters.length > 0 && (
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-2">
                Query Parameters
              </label>
              <div className="space-y-2">
                {endpoint.queryParameters.map((param: any) => (
                  <div key={param.name} className="flex gap-2">
                    <label className="text-xs text-slate-400 w-24 pt-2">{param.name}</label>
                    <Input
                      placeholder={param.description || 'Enter value'}
                      value={queryParams[param.name] || ''}
                      onChange={(e) =>
                        setQueryParams({
                          ...queryParams,
                          [param.name]: e.target.value
                        })
                      }
                      className="bg-slate-700 border-slate-600 text-white flex-1"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Request Body */}
          {endpoint.method !== 'GET' && endpoint.requestBody && (
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-2">
                Request Body
              </label>
              <div className="space-y-2">
                {Object.keys(endpoint.requestBody.schema || {}).map((fieldName) => (
                  <div key={fieldName} className="flex gap-2">
                    <label className="text-xs text-slate-400 w-24 pt-2">{fieldName}</label>
                    <Input
                      placeholder={`Enter ${fieldName}`}
                      value={requestBody[fieldName] || ''}
                      onChange={(e) =>
                        setRequestBody({
                          ...requestBody,
                          [fieldName]: e.target.value
                        })
                      }
                      className="bg-slate-700 border-slate-600 text-white flex-1"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Send Button */}
          <Button
            onClick={handleSendRequest}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Sending Request...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Send Request
              </>
            )}
          </Button>

          {/* cURL Example */}
          <div className="bg-slate-700 p-4 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <label className="text-sm font-semibold text-slate-300">cURL Command</label>
              <Button
                onClick={() => copyToClipboard(generateCurl())}
                variant="ghost"
                size="sm"
                className="gap-1"
              >
                <Copy className="w-3 h-3" />
                {copied ? 'Copied!' : 'Copy'}
              </Button>
            </div>
            <pre className="text-xs text-slate-300 overflow-x-auto whitespace-pre-wrap break-words">
              {generateCurl()}
            </pre>
          </div>
        </CardContent>
      </Card>

      {/* Test Result */}
      {testResult && (
        <Card className={`border-slate-700 ${testResult.status === 'completed' ? 'bg-green-900/20 border-green-700' : 'bg-red-900/20 border-red-700'}`}>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-white flex items-center gap-2">
                {testResult.status === 'completed' ? (
                  <>
                    <CheckCircle className="w-5 h-5 text-green-500" />
                    Response
                  </>
                ) : (
                  <>
                    <AlertCircle className="w-5 h-5 text-red-500" />
                    Error
                  </>
                )}
              </CardTitle>
              {testResult.status_code && (
                <Badge className={testResult.status_code < 400 ? 'bg-green-600' : 'bg-red-600'}>
                  {testResult.status_code}
                </Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {testResult.error && (
              <Alert className="bg-red-900 border-red-700">
                <AlertCircle className="h-4 w-4 text-red-200" />
                <AlertDescription className="text-red-200">{testResult.error}</AlertDescription>
              </Alert>
            )}

            {testResult.response_body && (
              <div>
                <label className="text-sm font-semibold text-slate-300 mb-2 block">Response Body</label>
                <pre className="bg-slate-700 p-4 rounded-lg text-xs text-slate-300 overflow-x-auto">
                  {JSON.stringify(testResult.response_body, null, 2)}
                </pre>
              </div>
            )}

            {testResult.execution_time && (
              <div className="text-xs text-slate-400">
                Execution time: {(testResult.execution_time * 1000).toFixed(2)}ms
              </div>
            )}

            {testResult.response_headers && (
              <div>
                <label className="text-sm font-semibold text-slate-300 mb-2 block">Response Headers</label>
                <div className="bg-slate-700 p-3 rounded-lg text-xs text-slate-300 space-y-1 max-h-40 overflow-y-auto">
                  {Object.entries(testResult.response_headers).map(([key, value]) => (
                    <div key={key} className="flex justify-between">
                      <span className="font-mono">{key}:</span>
                      <span className="text-slate-400">{String(value)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
