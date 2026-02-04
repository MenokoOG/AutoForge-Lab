// frontend/src/app/api.ts
export type CrawlRecord = {
    id: number;
    source: string;
    title: string;
    url: string;
    tags: string[];
    fetched_at: string;
    content_hash: string;
};

const DEFAULT_BASE_URL = "http://localhost:8000";

export function getApiBaseUrl(): string {
    // Vite exposes env vars on import.meta.env
    const env = (import.meta as any).env;
    const base = (env?.VITE_API_BASE_URL as string | undefined) ?? DEFAULT_BASE_URL;
    return base.replace(/\/+$/, "");
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
    const res = await fetch(url, init);
    if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(`HTTP ${res.status} ${res.statusText} - ${text}`.trim());
    }
    return (await res.json()) as T;
}

export async function getHealth(): Promise<{ ok: boolean }> {
    const base = getApiBaseUrl();
    return fetchJson<{ ok: boolean }>(`${base}/health`);
}

export async function getCrawlRecords(): Promise<CrawlRecord[]> {
    const base = getApiBaseUrl();
    return fetchJson<CrawlRecord[]>(`${base}/crawl/records`);
}