"use client";

import { ReactNode } from "react";

type Props = {
  title: string;
  description?: string;
  detected: boolean;
  children: ReactNode;
};

export default function DocFeatureSection({ title, description, detected, children }: Props) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4">
      <div className="flex items-start justify-between gap-2">
        <div>
          <h3 className="text-sm font-semibold text-slate-900">{title}</h3>
          {description ? <p className="mt-0.5 text-xs text-slate-500">{description}</p> : null}
        </div>
        <span
          className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide ${
            detected ? "bg-emerald-50 text-emerald-700" : "bg-slate-100 text-slate-500"
          }`}
        >
          {detected ? "detected" : "not detected"}
        </span>
      </div>
      <div className="mt-3 text-sm text-slate-800">{children}</div>
    </section>
  );
}
