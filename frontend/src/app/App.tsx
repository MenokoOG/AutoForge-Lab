// frontend/src/app/App.tsx
import { useEffect, useMemo, useRef, useState } from "react";
import "./App.css";
import {
  getApiBaseUrl,
  getCrawlRecords,
  getHealth,
  getJobs,
  runCrawlNow,
  type CrawlRecord,
  type JobRun,
} from "./api";

function formatUtc(ts?: string | null) {
  if (!ts) return "—";
  const d = new Date(ts);
  if (Number.isNaN(d.getTime())) return ts;
  return d.toISOString().replace("T", " ").replace("Z", " UTC");
}

function truncate(s: string, max = 160) {
  if (!s) return "";
  return s.length > max ? s.slice(0, max - 1) + "…" : s;
}

function uniqueSorted(xs: string[]) {
  return Array.from(new Set(xs))
    .filter(Boolean)
    .sort((a, b) => a.localeCompare(b));
}

export default function App() {
  const apiBase = useMemo(() => getApiBaseUrl(), []);

  // Health
  const [health, setHealth] = useState<{ ok: boolean } | null>(null);
  const [healthErr, setHealthErr] = useState<string | null>(null);

  // Records
  const [records, setRecords] = useState<CrawlRecord[]>([]);
  const [recordsErr, setRecordsErr] = useState<string | null>(null);
  const [loadingRecords, setLoadingRecords] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  // Jobs
  const [jobs, setJobs] = useState<JobRun[]>([]);
  const [jobsErr, setJobsErr] = useState<string | null>(null);
  const [loadingJobs, setLoadingJobs] = useState(false);

  // UI controls
  const [limit, setLimit] = useState(100);
  const [sourceFilter, setSourceFilter] = useState<string>("all");
  const [tagFilter, setTagFilter] = useState<string>("all");
  const [search, setSearch] = useState<string>("");

  // Auto refresh
  const [autoRefresh, setAutoRefresh] = useState<boolean>(false);
  const [refreshSeconds, setRefreshSeconds] = useState<number>(30);
  const intervalRef = useRef<number | null>(null);

  async function loadHealth() {
    setHealthErr(null);
    try {
      const h = await getHealth();
      setHealth(h);
    } catch (e: any) {
      setHealth(null);
      setHealthErr(e?.message ?? String(e));
    }
  }

  async function loadRecords() {
    setLoadingRecords(true);
    setRecordsErr(null);
    try {
      const rows = await getCrawlRecords(limit);
      setRecords(rows);
      setLastUpdated(new Date().toISOString());
    } catch (e: any) {
      setRecordsErr(e?.message ?? String(e));
    } finally {
      setLoadingRecords(false);
    }
  }

  async function loadJobs() {
    setLoadingJobs(true);
    setJobsErr(null);
    try {
      const js = await getJobs(20);
      setJobs(js);
    } catch (e: any) {
      setJobsErr(e?.message ?? String(e));
    } finally {
      setLoadingJobs(false);
    }
  }

  async function runNow() {
    // optimistic UX: show jobs refresh quickly
    setJobsErr(null);
    try {
      const res = await runCrawlNow();
      // refresh jobs + records shortly after
      await loadJobs();
      // give backend background task a moment to start
      setTimeout(() => void loadRecords(), 600);
      return res;
    } catch (e: any) {
      setJobsErr(e?.message ?? String(e));
      throw e;
    }
  }

  // Initial load
  useEffect(() => {
    void loadHealth();
    void loadRecords();
    void loadJobs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Auto-refresh interval wiring
  useEffect(() => {
    if (intervalRef.current) {
      window.clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    if (!autoRefresh) return;

    const ms = Math.max(5, Math.min(refreshSeconds, 600)) * 1000;
    intervalRef.current = window.setInterval(() => {
      void loadRecords();
      void loadJobs();
    }, ms);

    return () => {
      if (intervalRef.current) {
        window.clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoRefresh, refreshSeconds, limit]);

  const allSources = useMemo(
    () => uniqueSorted(records.map((r) => r.source)),
    [records],
  );
  const allTags = useMemo(
    () => uniqueSorted(records.flatMap((r) => r.tags ?? [])),
    [records],
  );

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    return records.filter((r) => {
      if (sourceFilter !== "all" && r.source !== sourceFilter) return false;
      if (tagFilter !== "all" && !(r.tags ?? []).includes(tagFilter))
        return false;

      if (!q) return true;
      const hay =
        `${r.title} ${r.url} ${(r.tags ?? []).join(" ")}`.toLowerCase();
      return hay.includes(q);
    });
  }, [records, sourceFilter, tagFilter, search]);

  return (
    <div className="app-shell">
      <div className="app-container">
        <div className="card">
          <h1>Learning Lounge Automation Stack</h1>

          <p className="muted">
            API base: <code>{apiBase}</code>
          </p>

          <div className="grid">
            <div className="card subtle">
              <h2 className="h2">Backend health</h2>
              {health && (
                <pre aria-label="health-json">{JSON.stringify(health)}</pre>
              )}
              {!health && healthErr && (
                <div role="alert" className="alert">
                  <div className="alert-title">Health check failed</div>
                  <div className="muted" style={{ whiteSpace: "pre-wrap" }}>
                    {healthErr}
                  </div>
                </div>
              )}
              <div className="row">
                <button className="btn" onClick={loadHealth}>
                  Re-check Health
                </button>
              </div>
            </div>

            <div className="card subtle">
              <h2 className="h2">Controls</h2>

              <div className="row">
                <button
                  className="btn"
                  onClick={loadRecords}
                  disabled={loadingRecords}
                >
                  {loadingRecords ? "Refreshing…" : "Refresh Records"}
                </button>

                <button
                  className="btn btn-primary"
                  onClick={() => void runNow()}
                >
                  Run Crawl Now
                </button>
              </div>

              <div className="row" style={{ marginTop: 10 }}>
                <label className="label">
                  Limit
                  <select
                    className="select"
                    value={limit}
                    onChange={(e) => setLimit(parseInt(e.target.value, 10))}
                  >
                    <option value={50}>50</option>
                    <option value={100}>100</option>
                    <option value={200}>200</option>
                    <option value={500}>500</option>
                  </select>
                </label>

                <label className="label">
                  Auto-refresh
                  <input
                    type="checkbox"
                    checked={autoRefresh}
                    onChange={(e) => setAutoRefresh(e.target.checked)}
                    style={{ marginLeft: 10 }}
                    aria-label="auto-refresh-toggle"
                  />
                </label>

                <label className="label">
                  Every (sec)
                  <input
                    className="input"
                    type="number"
                    min={5}
                    max={600}
                    value={refreshSeconds}
                    onChange={(e) =>
                      setRefreshSeconds(parseInt(e.target.value || "30", 10))
                    }
                    style={{ width: 90 }}
                    aria-label="auto-refresh-seconds"
                  />
                </label>
              </div>

              <div className="muted" style={{ marginTop: 10 }}>
                Last updated: <b>{formatUtc(lastUpdated)}</b>
              </div>
            </div>
          </div>
        </div>

        <div className="card" style={{ marginTop: 16 }}>
          <h2 className="h2">Filters</h2>

          <div className="row">
            <label className="label">
              Source
              <select
                className="select"
                value={sourceFilter}
                onChange={(e) => setSourceFilter(e.target.value)}
              >
                <option value="all">All</option>
                {allSources.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </label>

            <label className="label">
              Tag
              <select
                className="select"
                value={tagFilter}
                onChange={(e) => setTagFilter(e.target.value)}
              >
                <option value="all">All</option>
                {allTags.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </label>

            <label className="label grow">
              Search
              <input
                className="input"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="title, url, tag…"
                aria-label="search"
              />
            </label>

            <button
              className="btn"
              onClick={() => {
                setSourceFilter("all");
                setTagFilter("all");
                setSearch("");
              }}
            >
              Clear
            </button>
          </div>

          <div className="muted" style={{ marginTop: 10 }}>
            Showing <b>{filtered.length}</b> of <b>{records.length}</b>{" "}
            record(s).
          </div>

          {recordsErr && (
            <div role="alert" className="alert" style={{ marginTop: 12 }}>
              <div className="alert-title">Failed to load records</div>
              <div className="muted" style={{ whiteSpace: "pre-wrap" }}>
                {recordsErr}
              </div>
            </div>
          )}

          {!recordsErr && filtered.length > 0 && (
            <div style={{ overflowX: "auto", marginTop: 12 }}>
              <table className="table" aria-label="crawl-records-table">
                <thead>
                  <tr>
                    <th style={{ width: 70 }}>ID</th>
                    <th style={{ width: 120 }}>Source</th>
                    <th>Title</th>
                    <th style={{ width: 170 }}>Fetched</th>
                    <th style={{ width: 220 }}>Tags</th>
                    <th style={{ width: 90 }}>Link</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((r) => (
                    <tr key={r.id}>
                      <td>{r.id}</td>
                      <td>{r.source}</td>
                      <td title={r.title}>{truncate(r.title)}</td>
                      <td>{formatUtc(r.fetched_at)}</td>
                      <td>
                        {(r.tags ?? []).length === 0 ? (
                          <span className="muted">—</span>
                        ) : (
                          (r.tags ?? []).map((t) => (
                            <span key={`${r.id}-${t}`} className="badge">
                              {t}
                            </span>
                          ))
                        )}
                      </td>
                      <td>
                        <a href={r.url} target="_blank" rel="noreferrer">
                          Open
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {!recordsErr && filtered.length === 0 && (
            <div className="muted" style={{ marginTop: 12 }}>
              No matching records. Try clearing filters/search, or click{" "}
              <b>Run Crawl Now</b>.
            </div>
          )}
        </div>

        <div className="card" style={{ marginTop: 16 }}>
          <div className="row" style={{ justifyContent: "space-between" }}>
            <h2 className="h2">Recent Job Runs</h2>
            <button className="btn" onClick={loadJobs} disabled={loadingJobs}>
              {loadingJobs ? "Refreshing…" : "Refresh Jobs"}
            </button>
          </div>

          {jobsErr && (
            <div role="alert" className="alert" style={{ marginTop: 12 }}>
              <div className="alert-title">Jobs error</div>
              <div className="muted" style={{ whiteSpace: "pre-wrap" }}>
                {jobsErr}
              </div>
            </div>
          )}

          {!jobsErr && jobs.length > 0 && (
            <div style={{ overflowX: "auto", marginTop: 12 }}>
              <table className="table" aria-label="jobs-table">
                <thead>
                  <tr>
                    <th style={{ width: 70 }}>ID</th>
                    <th style={{ width: 160 }}>Name</th>
                    <th style={{ width: 120 }}>Status</th>
                    <th>Message</th>
                    <th style={{ width: 190 }}>Created</th>
                    <th style={{ width: 190 }}>Started</th>
                    <th style={{ width: 190 }}>Finished</th>
                  </tr>
                </thead>
                <tbody>
                  {jobs.map((j) => (
                    <tr key={j.id}>
                      <td>{j.id}</td>
                      <td>{j.name}</td>
                      <td>
                        <span className={`badge badge-${j.status}`}>
                          {j.status}
                        </span>
                      </td>
                      <td title={j.message ?? ""}>
                        {truncate(j.message ?? "—", 120)}
                      </td>
                      <td>{formatUtc(j.created_at)}</td>
                      <td>{formatUtc(j.started_at)}</td>
                      <td>{formatUtc(j.finished_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {!jobsErr && jobs.length === 0 && (
            <div className="muted" style={{ marginTop: 12 }}>
              No jobs yet. Click <b>Run Crawl Now</b> to create one.
            </div>
          )}

          <div className="muted" style={{ marginTop: 12 }}>
            Worker tip (legacy compose):
            <pre style={{ marginTop: 6 }}>
              {`docker-compose logs -f --tail=200 worker
docker-compose exec worker python -c "from app.scheduler.jobs import run_crawl_sampler; run_crawl_sampler(); print('done')"`}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
