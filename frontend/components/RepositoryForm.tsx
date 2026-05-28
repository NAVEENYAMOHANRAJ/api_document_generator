"use client";

import { useState } from "react";

interface RepositoryFormProps {
  onScan: (repoUrl: string, token: string) => void;
  onExtract: (repoUrl: string, token: string) => void;
  onExtractLocalFolder: (folderPath: string) => void;
  onExtractUpload: (file: File) => void;
  onCancel: () => void;
  loading: boolean;
  loadingLabel?: string;
}

export default function RepositoryForm({
  onScan,
  onExtract,
  onExtractLocalFolder,
  onExtractUpload,
  onCancel,
  loading,
  loadingLabel,
}: RepositoryFormProps) {
  const [inputMode, setInputMode] = useState<"github" | "local" | "upload">("github");
  const [repoUrl, setRepoUrl] = useState("");
  const [token, setToken] = useState("");
  const [showToken, setShowToken] = useState(false);
  const [folderPath, setFolderPath] = useState("");
  const [zipFile, setZipFile] = useState<File | null>(null);

  const handleScan = (e: React.FormEvent) => {
    e.preventDefault();
    if (repoUrl.trim()) {
      onScan(repoUrl, token);
    }
  };

  const handleExtract = (e: React.FormEvent) => {
    e.preventDefault();
    if (repoUrl.trim()) {
      onExtract(repoUrl, token);
    }
  };

  return (
    <form className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm space-y-5">
      <div className="flex flex-col gap-3 border-b border-slate-100 pb-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-950">Repository Source</h2>
          <p className="text-sm text-slate-500">Choose a GitHub repo, local folder, or ZIP archive.</p>
        </div>
        {loading && (
          <button
            type="button"
            onClick={onCancel}
            className="rounded-md border border-red-200 px-3 py-2 text-sm font-medium text-red-700 hover:bg-red-50"
          >
            Stop Request
          </button>
        )}
      </div>

      <div className="grid grid-cols-3 gap-2 rounded-lg bg-slate-100 p-1">
        {(["github", "local", "upload"] as const).map((mode) => (
          <button
            key={mode}
            type="button"
            onClick={() => setInputMode(mode)}
            className={`rounded-md px-3 py-2 text-sm font-medium ${
              inputMode === mode
                ? "bg-white text-slate-950 shadow-sm"
                : "text-slate-600 hover:text-slate-950"
            }`}
          >
            {mode === "github" ? "GitHub" : mode === "local" ? "Local Path" : "ZIP Upload"}
          </button>
        ))}
      </div>

      {inputMode === "github" && (
        <>
          <div>
            <label htmlFor="repo-url" className="block text-sm font-medium text-slate-700 mb-2">
              GitHub Repository URL
            </label>
            <input
              id="repo-url"
              type="text"
              placeholder="https://github.com/owner/repo or owner/repo"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              disabled={loading}
              className="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-blue-600 focus:ring-2 focus:ring-blue-100 disabled:bg-slate-100"
            />
          </div>

          <div>
            <label htmlFor="github-token" className="block text-sm font-medium text-slate-700 mb-2">
              GitHub Token (Optional)
            </label>
            <div className="relative">
              <input
                id="github-token"
                type={showToken ? "text" : "password"}
                placeholder="github_pat_... or personal access token"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                disabled={loading}
                className="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-blue-600 focus:ring-2 focus:ring-blue-100 disabled:bg-slate-100"
              />
              <button
                type="button"
                onClick={() => setShowToken(!showToken)}
                className="absolute right-3 top-2.5 text-slate-500 hover:text-blue-700"
              >
                {showToken ? "Hide" : "Show"}
              </button>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Used for private repositories. GitHub inputs are shallow-cloned into a temporary server folder, then removed after extraction.
            </p>
          </div>

          <div className="flex gap-4">
            <button
              type="button"
              onClick={handleScan}
              disabled={!repoUrl.trim()}
              className="flex-1 rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 font-semibold text-blue-800 transition hover:bg-blue-100 disabled:cursor-not-allowed disabled:border-slate-200 disabled:bg-slate-100 disabled:text-slate-400"
            >
              {loading ? loadingLabel || "Working..." : "Scan Repository"}
            </button>
            <button
              type="button"
              onClick={handleExtract}
              disabled={!repoUrl.trim()}
              className="flex-1 rounded-lg bg-slate-950 px-4 py-3 font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {loading ? loadingLabel || "Working..." : "Generate API Docs"}
            </button>
          </div>
        </>
      )}

      {inputMode === "local" && (
        <div className="space-y-4">
          <div>
            <label htmlFor="folder-path" className="block text-sm font-medium text-slate-700 mb-2">
              Server Local Folder Path
            </label>
            <input
              id="folder-path"
              type="text"
              placeholder="C:\\path\\to\\api-folder"
              value={folderPath}
              onChange={(e) => setFolderPath(e.target.value)}
              disabled={loading}
              className="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-blue-600 focus:ring-2 focus:ring-blue-100 disabled:bg-slate-100"
            />
          </div>
          <button
            type="button"
            onClick={(e) => {
              e.preventDefault();
              if (folderPath.trim()) onExtractLocalFolder(folderPath);
            }}
            disabled={!folderPath.trim()}
            className="w-full rounded-lg bg-slate-950 px-4 py-3 font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            {loading ? loadingLabel || "Working..." : "Generate API Docs"}
          </button>
        </div>
      )}

      {inputMode === "upload" && (
        <div className="space-y-4">
          <div>
            <label htmlFor="zip-upload" className="block text-sm font-medium text-slate-700 mb-2">
              Upload Codebase ZIP
            </label>
            <input
              id="zip-upload"
              type="file"
              accept=".zip"
              onChange={(e) => setZipFile(e.target.files?.[0] || null)}
              disabled={loading}
              className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2 disabled:bg-slate-100"
            />
          </div>
          <button
            type="button"
            onClick={(e) => {
              e.preventDefault();
              if (zipFile) onExtractUpload(zipFile);
            }}
            disabled={!zipFile}
            className="w-full rounded-lg bg-slate-950 px-4 py-3 font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            {loading ? loadingLabel || "Working..." : "Generate API Docs"}
          </button>
        </div>
      )}
    </form>
  );
}
