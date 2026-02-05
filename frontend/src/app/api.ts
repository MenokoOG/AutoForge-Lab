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

export type JobRun = {
    id: number;
    name: string;
    status: "queued" | "running" | "success" | "error" | string;
    message?: string | null;
    created_at?: string | null;
    started_at?: string | null;
    finished_at?: string | null;
};

const DEFAULT_BASE_URL = "http://localhost:8000";

export function getApiBaseUrl(): string {
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

export async function getCrawlRecords(limit: number = 100): Promise<CrawlRecord[]> {
    const base = getApiBaseUrl();
    const safe = Math.max(1, Math.min(limit, 500));
    return fetchJson<CrawlRecord[]>(`${base}/crawl/records?limit=${safe}`);
}

export async function runCrawlNow(): Promise<{ ok: boolean; job_id: number }> {
    const base = getApiBaseUrl();
    return fetchJson<{ ok: boolean; job_id: number }>(`${base}/crawl/run`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({}),
    });
}

export async function getJobs(limit: number = 20): Promise<JobRun[]> {
    const base = getApiBaseUrl();
    const safe = Math.max(1, Math.min(limit, 100));
    return fetchJson<JobRun[]>(`${base}/crawl/jobs?limit=${safe}`);
}