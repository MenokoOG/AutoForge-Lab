// frontend/src/app/App.tsx
import { useEffect, useMemo, useState } from "react";
import "./App.css";
import {
  getApiBaseUrl,
  getCrawlRecords,
  getHealth,
  type CrawlRecord,
} from "./api";

function formatUtc(ts: string) {
  // Keep it readable, always show UTC (your backend stores UTC)
  const d = new Date(ts);
  if (Number.isNaN(d.getTime())) return ts;
  return d.toISOString().replace("T", " ").replace("Z", " UTC");
}

function truncate(s: string, max = 120) {
  if (!s) return "";
  return s.length > max ? s.slice(0, max - 1) + "…" : s;
}

export default function App() {
  const apiBase = useMemo(() => getApiBaseUrl(), []);

  const [health, setHealth] = useState<{ ok: boolean } | null>(null);
  const [healthErr, setHealthErr] = useState<string | null>(null);

  const [records, setRecords] = useState<CrawlRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [recordsErr, setRecordsErr] = useState<string | null>(null);

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
    setLoading(true);
    setRecordsErr(null);
    try {
      const rows = await getCrawlRecords();
      setRecords(rows);
    } catch (e: any) {
      setRecordsErr(e?.message ?? String(e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadHealth();
    void loadRecords();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="app-shell">
      <div className="app-container">
        <div className="card">
          <h1>Learning Lounge Automation Stack</h1>

          <p className="muted">
            API base: <code>{apiBase}</code>
          </p>

          <div className="row" style={{ marginTop: 12 }}>
            <button className="btn" onClick={loadRecords} disabled={loading}>
              {loading ? "Refreshing…" : "Refresh Records"}
            </button>

            <button className="btn" onClick={loadHealth}>
              Re-check Health
            </button>
          </div>

          <div style={{ marginTop: 14 }}>
            <h2 style={{ fontSize: 16, marginBottom: 6 }}>Backend health</h2>

            {health && (
              <pre aria-label="health-json">{JSON.stringify(health)}</pre>
            )}

            {!health && healthErr && (
              <div role="alert" className="card" style={{ marginTop: 8 }}>
                <div style={{ fontWeight: 800, marginBottom: 6 }}>
                  Health check failed
                </div>
                <div className="muted" style={{ whiteSpace: "pre-wrap" }}>
                  {healthErr}
                </div>
                <div className="muted" style={{ marginTop: 10 }}>
                  Quick check:
                  <pre style={{ marginTop: 6 }}>
                    {`curl -fsS ${apiBase}/health && echo`}
                  </pre>
                </div>
              </div>
            )}
          </div>

          <div style={{ marginTop: 16 }}>
            <h2 style={{ fontSize: 16, marginBottom: 6 }}>Worker logs</h2>

            <p className="muted">
              You’re using legacy Compose (<code>docker-compose</code>). These
              commands work:
            </p>

            <pre aria-label="worker-logs-cmd" style={{ marginTop: 8 }}>
              {`docker-compose logs -f --tail=200 worker
docker-compose exec worker python -c "from app.scheduler.jobs import run_crawl_sampler; run_crawl_sampler(); print('done')"`}
            </pre>
          </div>
        </div>

        <div className="card" style={{ marginTop: 16 }}>
          <h2 style={{ fontSize: 18, marginBottom: 6 }}>Latest Records</h2>

          <p className="muted">
            Showing {records.length} record{records.length === 1 ? "" : "s"}.
          </p>

          {recordsErr && (
            <div role="alert" className="card" style={{ marginTop: 12 }}>
              <div style={{ fontWeight: 800, marginBottom: 6 }}>
                Failed to load records
              </div>
              <div className="muted" style={{ whiteSpace: "pre-wrap" }}>
                {recordsErr}
              </div>
              <div className="muted" style={{ marginTop: 10 }}>
                Quick check:
                <pre style={{ marginTop: 6 }}>
                  {`curl -fsS ${apiBase}/crawl/records | head -c 600 && echo`}
                </pre>
              </div>
            </div>
          )}

          {!recordsErr && records.length === 0 && (
            <div className="muted" style={{ marginTop: 12 }}>
              No records yet. If the DB has data but this shows empty, force-run
              the crawl job using the command above.
            </div>
          )}

          {!recordsErr && records.length > 0 && (
            <div style={{ overflowX: "auto", marginTop: 12 }}>
              <table className="table" aria-label="crawl-records-table">
                <thead>
                  <tr>
                    <th style={{ width: 70 }}>ID</th>
                    <th style={{ width: 110 }}>Source</th>
                    <th>Title</th>
                    <th style={{ width: 170 }}>Fetched</th>
                    <th style={{ width: 210 }}>Tags</th>
                    <th style={{ width: 90 }}>Link</th>
                  </tr>
                </thead>
                <tbody>
                  {records.map((r) => (
                    <tr key={r.id}>
                      <td>{r.id}</td>
                      <td>{r.source}</td>
                      <td title={r.title}>{truncate(r.title, 160)}</td>
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

              <p className="muted" style={{ marginTop: 10 }}>
                Tip: you already confirmed the DB has data (count &gt; 0). This
                table should always show rows once the API is reachable.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
