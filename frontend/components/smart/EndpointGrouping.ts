export type EndpointLike = Record<string, unknown>;

export type EndpointGroup = {
  id: string;
  title: string;
  endpoints: EndpointLike[];
};

function safeString(v: unknown): string {
  return typeof v === "string" ? v : v == null ? "" : String(v);
}

export function endpointKey(ep: EndpointLike): string {
  return safeString((ep as any).id) || `${safeString(ep.method)} ${safeString(ep.path)} ${safeString(ep.source_file)}`;
}

export function groupEndpoints(endpoints: EndpointLike[]): EndpointGroup[] {
  const groups = new Map<string, EndpointLike[]>();

  for (const ep of endpoints) {
    const path = safeString(ep.path);
    const parts = path.replace(/^\//, "").split("/").filter(Boolean);
    const group = (parts[0] && !parts[0].startsWith("{")) ? parts[0] : "root";
    const title = group === "root" ? "Root" : group.charAt(0).toUpperCase() + group.slice(1);
    const id = title.toLowerCase();
    if (!groups.has(id)) groups.set(id, []);
    groups.get(id)!.push(ep);
  }

  const result: EndpointGroup[] = [];
  for (const [id, eps] of groups.entries()) {
    const title = id === "root" ? "Root" : id.charAt(0).toUpperCase() + id.slice(1);
    result.push({ id, title, endpoints: eps });
  }

  result.sort((a, b) => a.title.localeCompare(b.title));
  for (const g of result) {
    g.endpoints.sort((a, b) => {
      const am = safeString(a.method).localeCompare(safeString(b.method));
      if (am !== 0) return am;
      return safeString(a.path).localeCompare(safeString(b.path));
    });
  }
  return result;
}

