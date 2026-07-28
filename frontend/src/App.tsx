// frontend/src/App.tsx
import { useState, useEffect } from "react";
import { 
  Activity, Cpu, ShieldCheck, DollarSign, Command, Search, 
  CheckCircle, Play, Download, Power, Users, Wifi, WifiOff, 
  ArrowUpRight 
} from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  
  // Real-time State Mocking
  const [healthScore, setHealthScore] = useState(88);
  const [activeIncidentsCount, setActiveIncidentsCount] = useState(3);
  const [totalCostMonthly] = useState(2580.00);
  const [monthlySavingsEst, setMonthlySavingsEst] = useState(250.00);
  
  // Incidents
  const [incidents, setIncidents] = useState([
    { id: "inc-1", title: "Memory Leak: app-server container pool", status: "Triggered", severity: "Critical" },
    { id: "inc-2", title: "Latency spikes on db-prod-read-replica", status: "Investigating", severity: "Warning" },
    { id: "inc-3", title: "Kubernetes node resource pressure: us-west-2", status: "Triggered", severity: "Critical" }
  ]);

  // Approvals
  const [approvals, setApprovals] = useState([
    { id: "app-1", action: "scale_down", resource: "i-0123456789abcdef0", risk: 90, status: "pending" },
    { id: "app-2", action: "restart_service", resource: "db-prod-postgres", risk: 45, status: "pending" }
  ]);

  // AIOps Anomaly Check
  const [zScoreMetric, setZScoreMetric] = useState<number[]>([10.0, 12.0, 11.0, 13.0, 95.0]);
  const [anomalyResult, setAnomalyResult] = useState<any>(null);

  // RAG Search
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [uploadTitle, setUploadTitle] = useState("");
  const [uploadContent, setUploadContent] = useState("");

  // Automation Workflows
  const [workflows] = useState([
    { id: "wf-1", name: "Remediate CPU Overload Alert", trigger: "Alert", status: "Published" },
    { id: "wf-2", name: "Perform Security Group Audits", trigger: "Schedule", status: "Draft" }
  ]);
  const [workflowNodes] = useState([
    { id: "node-1", type: "Trigger", label: "CPU Threshold Alert", x: 20, y: 180 },
    { id: "node-2", type: "HTTP", label: "Query Metric Server", x: 220, y: 100 },
    { id: "node-3", type: "Approval", label: "Verify Downsizing Scale", x: 220, y: 260 },
    { id: "node-4", type: "Python", label: "Perform Hot Restart", x: 450, y: 180 }
  ]);
  const [workflowLogs, setWorkflowLogs] = useState<string[]>([]);
  
  // MLOps prompts versioning
  const [prompts] = useState([
    { key: "sre_diagnostic", version: "v1.2", template: "Investigate following system alert: {{alert_title}}" }
  ]);

  // LTS features
  const [cspEnabled] = useState(true);

  // Sync / Heartbeat state
  const [syncHistory, setSyncHistory] = useState<string[]>(["Initial local sync completed successfully."]);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      setSyncHistory(prev => [...prev, "Network restored. Synced cached entities with central DB."]);
    };
    const handleOffline = () => {
      setIsOnline(false);
      setSyncHistory(prev => [...prev, "Network lost. Switching local operations to IndexedDB cache."]);
    };
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    
    // Register Service Worker
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/sw.js")
        .then(() => console.log("Service Worker registered successfully"))
        .catch(err => console.error("Service Worker registration failed:", err));
    }

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  const handleMitigateIncident = (id: string) => {
    setIncidents(prev => prev.filter(i => i.id !== id));
    setActiveIncidentsCount(c => Math.max(0, c - 1));
    setHealthScore(prev => Math.min(100, prev + 4));
    setSyncHistory(prev => [...prev, `Mitigated incident alert: ${id}`]);
  };

  const handleApproveAction = (id: string, approve: boolean) => {
    setApprovals(prev => prev.filter(a => a.id !== id));
    if (approve) {
      setHealthScore(prev => Math.min(100, prev + 3));
      setSyncHistory(prev => [...prev, `Approved scaling action ticket: ${id}`]);
    } else {
      setSyncHistory(prev => [...prev, `Rejected action ticket: ${id}`]);
    }
  };

  const triggerAnomalyRun = () => {
    // Z-score calculation
    const mean = zScoreMetric.reduce((a, b) => a + b, 0) / zScoreMetric.length;
    const variance = zScoreMetric.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / zScoreMetric.length;
    const std = Math.sqrt(variance);
    const latest = zScoreMetric[zScoreMetric.length - 1];
    const z = std > 0 ? Math.abs((latest - mean) / std) : 0;
    
    setAnomalyResult({
      anomalous: z > 1.5,
      score: z.toFixed(2),
      latest_value: latest,
      mean: mean.toFixed(2),
      std: std.toFixed(2)
    });
  };

  const runWorkflow = (id: string) => {
    setWorkflowLogs([
      `Initializing run sequence for workflow ${id}...`,
      "Evaluating DAG nodes triggers...",
      "Evaluating Node [node-1] CPU Threshold Alert: Triggered.",
      "Evaluating Node [node-2] Query Metric Server: HTTP status code 200.",
      "Evaluating Node [node-3] Verify Downsizing Scale: Bypassed via waiver exception.",
      "Evaluating Node [node-4] Perform Hot Restart: Python script executed successfully.",
      "Workflow run completed."
    ]);
  };

  const executeRAGSearch = () => {
    if (!searchQuery) return;
    setSearchResults([
      {
        score: 0.94,
        content: `Runbook K8S-CPU-04: If target ${searchQuery} exceeds SLO metrics, verify memory limits and run horizontal scale steps.`,
        metadata: { chunk_index: 0, file: "k8s_scale_runbook.md" }
      },
      {
        score: 0.72,
        content: `Troubleshoot guidelines for general CPU spikes: isolate the faulty container and restart the service pool.`,
        metadata: { chunk_index: 2, file: "cpu_guide.md" }
      }
    ]);
  };

  const triggerShutdown = () => {
    alert("Server graceful shutdown command sent. Platforms resources are clean.");
  };

  const downloadDiagnostics = () => {
    // Generate mock CSV content and trigger download
    const data = "Application log bundle\nTime: 2026-07-27\nReadiness check: PASS\n";
    const blob = new Blob([data], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "aegisops_diagnostics_bundle.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <div className="sidebar">
        <div className="logo-container">
          <Activity size={24} color="#6366f1" />
          <span className="logo-text">AegisOps</span>
          <span className="logo-badge">v2.0</span>
        </div>
        
        <ul className="nav-links">
          <li 
            className={`nav-item ${activeTab === "dashboard" ? "active" : ""}`}
            onClick={() => setActiveTab("dashboard")}
          >
            <Activity size={18} />
            Executive Dashboard
          </li>
          <li 
            className={`nav-item ${activeTab === "aiops" ? "active" : ""}`}
            onClick={() => setActiveTab("aiops")}
          >
            <Cpu size={18} />
            AIOps Predictive
          </li>
          <li 
            className={`nav-item ${activeTab === "agents" ? "active" : ""}`}
            onClick={() => setActiveTab("agents")}
          >
            <Users size={18} />
            Autonomous Agents
          </li>
          <li 
            className={`nav-item ${activeTab === "automation" ? "active" : ""}`}
            onClick={() => setActiveTab("automation")}
          >
            <Command size={18} />
            Automation Studio
          </li>
          <li 
            className={`nav-item ${activeTab === "finops" ? "active" : ""}`}
            onClick={() => setActiveTab("finops")}
          >
            <DollarSign size={18} />
            FinOps & Budgeting
          </li>
          <li 
            className={`nav-item ${activeTab === "rag" ? "active" : ""}`}
            onClick={() => setActiveTab("rag")}
          >
            <Search size={18} />
            Knowledge RAG
          </li>
          <li 
            className={`nav-item ${activeTab === "governance" ? "active" : ""}`}
            onClick={() => setActiveTab("governance")}
          >
            <ShieldCheck size={18} />
            Governance & LTS
          </li>
        </ul>

        <div className="sidebar-footer">
          <div className="status-indicator">
            <span className={`status-dot ${isOnline ? "" : "offline"}`} />
            <span>{isOnline ? "PWA Online Sync" : "PWA Offline Mode"}</span>
            {isOnline ? <Wifi size={14} color="#10b981" /> : <WifiOff size={14} color="#ef4444" />}
          </div>
        </div>
      </div>

      {/* Main Workspace */}
      <div className="main-workspace">
        <div className="top-header">
          <h1 className="page-title">
            {activeTab === "dashboard" && "Executive Operations Center"}
            {activeTab === "aiops" && "AIOps Predictive Analytics"}
            {activeTab === "agents" && "Multi-Agent Orchestrator"}
            {activeTab === "automation" && "Automation Studio Workflow Designer"}
            {activeTab === "finops" && "FinOps Cost Optimization"}
            {activeTab === "rag" && "Enterprise Knowledge Base & RAG"}
            {activeTab === "governance" && "Governance, Compliance & Release Hardening"}
          </h1>
          <div className="glass-panel" style={{ padding: "8px 16px", fontSize: "14px", display: "flex", gap: "8px", alignItems: "center" }}>
            <span style={{ color: "var(--text-secondary)" }}>Grid Carbon Index:</span>
            <span className="badge success" style={{ textTransform: "none" }}>0.12 kg/kWh (Clean Grid)</span>
          </div>
        </div>

        {/* --- TAB 1: EXECUTIVE DASHBOARD --- */}
        {activeTab === "dashboard" && (
          <div>
            <div className="grid-container">
              <div className="glass-panel metric-card">
                <div className="metric-label">Composite Health Score</div>
                <div className={`metric-value ${healthScore > 85 ? "success" : "warning"}`}>{healthScore}%</div>
                <div className="metric-trend" style={{ color: "var(--color-success)" }}>
                  <ArrowUpRight size={14} /> +2.5% vs yesterday
                </div>
              </div>
              <div className="glass-panel metric-card">
                <div className="metric-label">Active Incidents</div>
                <div className={`metric-value ${activeIncidentsCount > 0 ? "danger" : "success"}`}>{activeIncidentsCount}</div>
                <div className="metric-trend" style={{ color: "var(--text-secondary)" }}>
                  {activeIncidentsCount > 0 ? "Requires SRE mitigation" : "System fully healthy"}
                </div>
              </div>
              <div className="glass-panel metric-card">
                <div className="metric-label">Est Monthly Spend</div>
                <div className="metric-value">${totalCostMonthly.toFixed(2)}</div>
                <div className="metric-trend" style={{ color: "var(--color-success)" }}>
                  Active Savings: ${monthlySavingsEst} saved
                </div>
              </div>
            </div>

            <div className="dashboard-section glass-panel" style={{ padding: "24px", marginBottom: "32px" }}>
              <h2 className="section-title">Active SRE Alerts & Incidents</h2>
              {incidents.length > 0 ? (
                <table className="custom-table">
                  <thead>
                    <tr>
                      <th>Title</th>
                      <th>Severity</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {incidents.map((i) => (
                      <tr key={i.id}>
                        <td style={{ fontWeight: 600 }}>{i.title}</td>
                        <td>
                          <span className={`badge ${i.severity === "Critical" ? "danger" : "warning"}`}>{i.severity}</span>
                        </td>
                        <td>{i.status}</td>
                        <td>
                          <button className="btn btn-secondary" onClick={() => handleMitigateIncident(i.id)}>
                            Mitigate Alert
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <div style={{ textAlign: "center", color: "var(--text-secondary)", padding: "24px" }}>
                  <CheckCircle size={36} color="var(--color-success)" style={{ marginBottom: "8px" }} />
                  <p>All clear. No active alerts.</p>
                </div>
              )}
            </div>

            <div className="dashboard-section glass-panel" style={{ padding: "24px" }}>
              <h2 className="section-title">PWA Sync / Offline Log</h2>
              <div style={{ background: "rgba(0,0,0,0.2)", borderRadius: "8px", padding: "16px", maxHeight: "180px", overflowY: "auto" }}>
                {syncHistory.map((s, idx) => (
                  <div key={idx} style={{ fontSize: "13px", color: "var(--text-secondary)", marginBottom: "6px", fontFamily: "var(--font-mono)" }}>
                    &gt; {s}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* --- TAB 2: AIOPS & PREDICTIVE --- */}
        {activeTab === "aiops" && (
          <div className="grid-container" style={{ gridTemplateColumns: "2fr 1fr" }}>
            <div className="glass-panel" style={{ padding: "24px" }}>
              <h2 className="section-title">Statistical Anomaly Detector</h2>
              <p style={{ color: "var(--text-secondary)", marginBottom: "16px", fontSize: "14px" }}>
                Z-Score algorithm analyzes metric series values inputs to detect anomalies.
              </p>
              
              <div style={{ display: "flex", gap: "12px", marginBottom: "20px" }}>
                <input 
                  type="text" 
                  value={zScoreMetric.join(", ")}
                  onChange={(e) => setZScoreMetric(e.target.value.split(",").map(v => parseFloat(v) || 0))}
                  style={{
                    background: "rgba(255,255,255,0.05)",
                    border: "1px solid var(--border-color)",
                    borderRadius: "8px",
                    color: "var(--text-primary)",
                    padding: "10px",
                    flexGrow: 1,
                    fontFamily: "var(--font-mono)"
                  }}
                />
                <button className="btn btn-primary" onClick={triggerAnomalyRun}>
                  Run Z-Score
                </button>
              </div>

              {anomalyResult && (
                <div style={{ background: "rgba(0,0,0,0.2)", borderRadius: "8px", padding: "16px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
                    <span>Anomaly Detected:</span>
                    <span className={`badge ${anomalyResult.anomalous ? "danger" : "success"}`}>
                      {anomalyResult.anomalous ? "Yes" : "No"}
                    </span>
                  </div>
                  <div style={{ fontSize: "13px", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "4px" }}>
                    <span>Z-Score Value: <strong>{anomalyResult.score}</strong></span>
                    <span>Mean Value: <strong>{anomalyResult.mean}</strong></span>
                    <span>Std Dev: <strong>{anomalyResult.std}</strong></span>
                  </div>
                </div>
              )}

              {/* Forecast SVG Chart */}
              <div style={{ marginTop: "32px" }}>
                <h3 className="section-title" style={{ fontSize: "16px" }}>Capacity Growth Trend Forecast</h3>
                <svg width="100%" height="150" style={{ background: "rgba(0,0,0,0.2)", borderRadius: "8px" }}>
                  <line x1="10%" y1="10%" x2="90%" y2="10%" stroke="rgba(255,255,255,0.03)" />
                  <line x1="10%" y1="50%" x2="90%" y2="50%" stroke="rgba(255,255,255,0.03)" />
                  <line x1="10%" y1="90%" x2="90%" y2="90%" stroke="rgba(255,255,255,0.03)" />
                  <polyline
                    fill="none"
                    stroke="#6366f1"
                    strokeWidth="3"
                    points="50,130 150,110 250,90 350,80 450,50"
                  />
                  <line x1="450" y1="50" x2="600" y2="20" stroke="#ef4444" strokeWidth="2" strokeDasharray="5,5" />
                  <text x="50" y="145" fill="var(--text-muted)" fontSize="10">Now</text>
                  <text x="450" y="145" fill="var(--text-muted)" fontSize="10">+24h (Est Exhaustion)</text>
                </svg>
              </div>
            </div>

            <div className="glass-panel" style={{ padding: "24px" }}>
              <h2 className="section-title">Predictive Insights</h2>
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div style={{ padding: "12px", borderLeft: "4px solid var(--color-danger)", background: "rgba(239, 68, 68, 0.05)" }}>
                  <h4 style={{ fontSize: "14px", fontWeight: 700, color: "var(--color-danger)" }}>High Risk: Node i-039c2</h4>
                  <p style={{ fontSize: "12px", color: "var(--text-secondary)" }}>
                    Failure probability: 85%. Prediction: Disk exhaustion imminent. Action: scale cluster node pool.
                  </p>
                </div>
                <div style={{ padding: "12px", borderLeft: "4px solid var(--color-warning)", background: "rgba(245, 158, 11, 0.05)" }}>
                  <h4 style={{ fontSize: "14px", fontWeight: 700, color: "var(--color-warning)" }}>Med Risk: DB replica</h4>
                  <p style={{ fontSize: "12px", color: "var(--text-secondary)" }}>
                    Failure probability: 40%. Prediction: Memory limit overrun. Action: Optimize read queries.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* --- TAB 3: AGENTS ORCHESTRATION --- */}
        {activeTab === "agents" && (
          <div>
            <div className="grid-container" style={{ gridTemplateColumns: "2fr 1fr" }}>
              {/* Agent Active Plan */}
              <div className="glass-panel" style={{ padding: "24px" }}>
                <h2 className="section-title">Active AI Agent Sessions</h2>
                <div className="timeline-logs">
                  <div className="timeline-item">
                    <div className="timeline-icon-container">
                      <Play size={14} color="#6366f1" />
                    </div>
                    <div className="timeline-content">
                      <div className="timeline-header">
                        <span className="timeline-sender">SREAgent</span>
                        <span className="timeline-time">Running Step 2/10</span>
                      </div>
                      <div className="timeline-body">
                        Assessing root causes of the database memory overload alert. Querying similarity indexes from the knowledge platform database.
                      </div>
                    </div>
                  </div>
                  <div className="timeline-item">
                    <div className="timeline-icon-container">
                      <Play size={14} color="#a855f7" />
                    </div>
                    <div className="timeline-content">
                      <div className="timeline-header">
                        <span className="timeline-sender">DevOpsAgent</span>
                        <span className="timeline-time">Step Completed</span>
                      </div>
                      <div className="timeline-body">
                        Generated Dockerfile deployment build package. Passed output files validations checks.
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Pending approvals */}
              <div className="glass-panel" style={{ padding: "24px" }}>
                <h2 className="section-title">Pending Human Approval</h2>
                {approvals.length > 0 ? (
                  <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                    {approvals.map((app) => (
                      <div key={app.id} style={{ background: "rgba(0,0,0,0.2)", padding: "16px", borderRadius: "12px", border: "1px solid var(--border-color)" }}>
                        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
                          <span style={{ fontWeight: 700, fontSize: "14px", textTransform: "uppercase" }}>{app.action}</span>
                          <span className={`badge ${app.risk > 80 ? "danger" : "warning"}`}>Risk {app.risk}%</span>
                        </div>
                        <div style={{ fontSize: "12px", color: "var(--text-secondary)", marginBottom: "12px" }}>
                          Target: {app.resource}
                        </div>
                        <div style={{ display: "flex", gap: "8px" }}>
                          <button className="btn btn-primary" style={{ padding: "6px 12px", fontSize: "12px" }} onClick={() => handleApproveAction(app.id, true)}>
                            Approve
                          </button>
                          <button className="btn btn-secondary" style={{ padding: "6px 12px", fontSize: "12px" }} onClick={() => handleApproveAction(app.id, false)}>
                            Reject
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div style={{ textAlign: "center", color: "var(--text-secondary)", padding: "24px" }}>
                    <CheckCircle size={28} color="var(--color-success)" style={{ marginBottom: "8px" }} />
                    <p>All operations approved</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* --- TAB 4: AUTOMATION STUDIO --- */}
        {activeTab === "automation" && (
          <div>
            <div className="grid-container" style={{ gridTemplateColumns: "3fr 2fr" }}>
              <div className="glass-panel" style={{ padding: "24px" }}>
                <h2 className="section-title">Visual Workflow Designer</h2>
                <div className="designer-canvas">
                  {workflowNodes.map(node => (
                    <div key={node.id} className="designer-node" style={{ left: node.x, top: node.y }}>
                      <div className="designer-node-header">{node.type} Node</div>
                      <div style={{ fontSize: "12px", fontWeight: 500 }}>{node.label}</div>
                    </div>
                  ))}
                  <svg style={{ position: "absolute", width: "100%", height: "100%", pointerEvents: "none", zIndex: 0 }}>
                    <path d="M 120 180 Q 170 140 220 100" fill="none" stroke="rgba(99, 102, 241, 0.4)" strokeWidth="2" />
                    <path d="M 120 180 Q 170 220 220 260" fill="none" stroke="rgba(99, 102, 241, 0.4)" strokeWidth="2" />
                    <path d="M 380 100 Q 410 140 450 180" fill="none" stroke="rgba(99, 102, 241, 0.4)" strokeWidth="2" />
                    <path d="M 380 260 Q 410 220 450 180" fill="none" stroke="rgba(99, 102, 241, 0.4)" strokeWidth="2" />
                  </svg>
                </div>
              </div>

              <div className="glass-panel" style={{ padding: "24px" }}>
                <h2 className="section-title">Workflow Manager</h2>
                <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                  {workflows.map(wf => (
                    <div key={wf.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "rgba(0,0,0,0.2)", padding: "16px", borderRadius: "12px" }}>
                      <div>
                        <h4 style={{ fontSize: "14px", fontWeight: 700 }}>{wf.name}</h4>
                        <span style={{ fontSize: "11px", color: "var(--text-secondary)" }}>Trigger: {wf.trigger}</span>
                      </div>
                      <button className="btn btn-primary" style={{ padding: "8px 12px" }} onClick={() => runWorkflow(wf.id)}>
                        Run DAG
                      </button>
                    </div>
                  ))}
                </div>

                {workflowLogs.length > 0 && (
                  <div style={{ marginTop: "24px" }}>
                    <h3 className="section-title" style={{ fontSize: "14px" }}>Execution Logs</h3>
                    <div style={{ background: "#000", padding: "12px", borderRadius: "8px", fontFamily: "var(--font-mono)", fontSize: "11px", maxHeight: "150px", overflowY: "auto" }}>
                      {workflowLogs.map((log, idx) => (
                        <div key={idx} style={{ color: log.includes("Failed") ? "var(--color-danger)" : "var(--text-secondary)", marginBottom: "4px" }}>
                          {log}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* --- TAB 5: FINOPS --- */}
        {activeTab === "finops" && (
          <div>
            <div className="grid-container">
              <div className="glass-panel metric-card">
                <div className="metric-label">Compute Spend (AWS)</div>
                <div className="metric-value">$1,850.00</div>
              </div>
              <div className="glass-panel metric-card">
                <div className="metric-label">Storage Spend (GCP)</div>
                <div className="metric-value">$580.00</div>
              </div>
              <div className="glass-panel metric-card">
                <div className="metric-label">Estimated Savings Potential</div>
                <div className="metric-value success">${monthlySavingsEst}</div>
              </div>
            </div>

            <div className="glass-panel" style={{ padding: "24px" }}>
              <h2 className="section-title">Rightsizing Recommendations</h2>
              <table className="custom-table">
                <thead>
                  <tr>
                    <th>Resource</th>
                    <th>Reason</th>
                    <th>Mitigation Recommendation</th>
                    <th>Est. Savings</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style={{ fontWeight: 600 }}>i-0123456789abcdef0</td>
                    <td>Average CPU under 5% over 7 days.</td>
                    <td>Downsize t3.large to t3.small.</td>
                    <td style={{ color: "var(--color-success)", fontWeight: 700 }}>$25.00/mo</td>
                    <td>
                      <button className="btn btn-secondary" style={{ padding: "6px 12px", fontSize: "12px" }} onClick={() => {
                        setMonthlySavingsEst(prev => prev + 25);
                        alert("Optimized compute instance resources configuration.");
                      }}>
                        Optimize Cost
                      </button>
                    </td>
                  </tr>
                  <tr>
                    <td style={{ fontWeight: 600 }}>db-prod-replica</td>
                    <td>Database read replica under 10% usage.</td>
                    <td>Downsize instance size.</td>
                    <td style={{ color: "var(--color-success)", fontWeight: 700 }}>$110.00/mo</td>
                    <td>
                      <button className="btn btn-secondary" style={{ padding: "6px 12px", fontSize: "12px" }} onClick={() => {
                        setMonthlySavingsEst(prev => prev + 110);
                        alert("Optimized database storage size configuration.");
                      }}>
                        Optimize Cost
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* --- TAB 6: RAG KNOWLEDGE BASE --- */}
        {activeTab === "rag" && (
          <div className="grid-container" style={{ gridTemplateColumns: "1fr 1fr" }}>
            {/* Search */}
            <div className="glass-panel" style={{ padding: "24px" }}>
              <h2 className="section-title">Query Knowledge base runbooks</h2>
              <div style={{ display: "flex", gap: "12px", marginBottom: "20px" }}>
                <input 
                  type="text" 
                  placeholder="Enter keywords (e.g. CPU spikes, memory leaks)..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  style={{
                    background: "rgba(255,255,255,0.05)",
                    border: "1px solid var(--border-color)",
                    borderRadius: "8px",
                    color: "var(--text-primary)",
                    padding: "10px",
                    flexGrow: 1
                  }}
                />
                <button className="btn btn-primary" onClick={executeRAGSearch}>
                  Search RAG
                </button>
              </div>

              {searchResults.length > 0 ? (
                <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                  {searchResults.map((res, idx) => (
                    <div key={idx} style={{ background: "rgba(255,255,255,0.02)", border: "1px solid var(--border-color)", padding: "16px", borderRadius: "12px" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                        <span style={{ fontSize: "12px", fontWeight: 700, color: "var(--accent-primary)" }}>{res.metadata.file}</span>
                        <span className="badge success">Score {res.score}</span>
                      </div>
                      <p style={{ fontSize: "13px", color: "var(--text-secondary)", lineHeight: 1.4 }}>{res.content}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ color: "var(--text-muted)", fontSize: "13px", textAlign: "center", padding: "24px" }}>
                  Enter keywords above to retrieve context.
                </div>
              )}
            </div>

            {/* Ingest */}
            <div className="glass-panel" style={{ padding: "24px" }}>
              <h2 className="section-title">Ingest Document</h2>
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div>
                  <label style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-secondary)", display: "block", marginBottom: "6px" }}>Document Title</label>
                  <input 
                    type="text"
                    placeholder="E.g., kubernetes_scale_guide.md"
                    value={uploadTitle}
                    onChange={(e) => setUploadTitle(e.target.value)}
                    style={{
                      background: "rgba(255,255,255,0.05)",
                      border: "1px solid var(--border-color)",
                      borderRadius: "8px",
                      color: "var(--text-primary)",
                      padding: "10px",
                      width: "100%"
                    }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-secondary)", display: "block", marginBottom: "6px" }}>Markdown Contents</label>
                  <textarea
                    rows={6}
                    placeholder="Enter manual standard operating guidelines or commands here..."
                    value={uploadContent}
                    onChange={(e) => setUploadContent(e.target.value)}
                    style={{
                      background: "rgba(255,255,255,0.05)",
                      border: "1px solid var(--border-color)",
                      borderRadius: "8px",
                      color: "var(--text-primary)",
                      padding: "10px",
                      width: "100%",
                      fontFamily: "var(--font-mono)",
                      fontSize: "13px"
                    }}
                  />
                </div>
                <button className="btn btn-primary" onClick={() => {
                  if (uploadTitle && uploadContent) {
                    alert("Document ingested, chunked, and vector indices added successfully.");
                    setUploadTitle("");
                    setUploadContent("");
                  }
                }}>
                  Upload Runbook
                </button>
              </div>
            </div>
          </div>
        )}

        {/* --- TAB 7: GOVERNANCE & LTS --- */}
        {activeTab === "governance" && (
          <div>
            <div className="grid-container">
              <div className="glass-panel metric-card">
                <div className="metric-label">Policy-as-Code checks</div>
                <div className="metric-value success">Active</div>
              </div>
              <div className="glass-panel metric-card">
                <div className="metric-label">Framework Compliance score</div>
                <div className="metric-value info">SOC2 / CIS (94%)</div>
              </div>
            </div>

            <div className="grid-container" style={{ gridTemplateColumns: "2fr 1fr" }}>
              <div className="glass-panel" style={{ padding: "24px" }}>
                <h2 className="section-title">LTS Operations & Release Hardening</h2>
                <p style={{ color: "var(--text-secondary)", marginBottom: "20px", fontSize: "14px" }}>
                  Hardening tools for managing production compliance audits, backups, and server lifecycle states.
                </p>

                <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
                  <button className="btn btn-secondary" onClick={downloadDiagnostics}>
                    <Download size={16} /> Download Diagnostics Bundle
                  </button>
                  <button className="btn btn-danger" onClick={triggerShutdown}>
                    <Power size={16} /> Graceful Shutdown
                  </button>
                </div>
                
                {/* MLOps registered prompts and variables check */}
                <div style={{ marginTop: "24px" }}>
                  <h3 className="section-title" style={{ fontSize: "15px" }}>MLOps Prompt Version Catalog</h3>
                  <table className="custom-table" style={{ fontSize: "13px" }}>
                    <thead>
                      <tr>
                        <th>Key</th>
                        <th>Version</th>
                        <th>Template</th>
                      </tr>
                    </thead>
                    <tbody>
                      {prompts.map((p, idx) => (
                        <tr key={idx}>
                          <td style={{ fontWeight: 600 }}>{p.key}</td>
                          <td><span className="badge info">{p.version}</span></td>
                          <td>{p.template}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="glass-panel" style={{ padding: "24px" }}>
                <h2 className="section-title">Security & CSP Headers</h2>
                <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span>CSP Headers status:</span>
                    <span className="badge success">{cspEnabled ? "Enforced" : "Disabled"}</span>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span>X-Frame-Options:</span>
                    <span className="badge success">DENY</span>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span>X-Content-Type-Options:</span>
                    <span className="badge success">nosniff</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
