"use client";

import { ReactNode } from "react";

export default function SmartShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-[1600px]">{children}</div>
    </div>
  );
}

