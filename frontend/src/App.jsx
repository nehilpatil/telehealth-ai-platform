import { useState, useEffect } from "react";
import "./App.css";
import api from "./api";
import { LoginPage } from "./LoginPage";
import { ClinicianDashboard } from "./ClinicianDashboard";
import { AdminDashboard } from "./AdminDashboard";

const RISK_META = {
  HIGH: { label: "High", color: "risk-high" },
  MEDIUM: { label: "Medium", color: "risk-medium" },
  LOW: { label: "Low", color: "risk-low" },
};

function RiskBadge({ level }) {
  const meta = RISK_META[level?.toUpperCase()] ?? { label: level, color: "risk-unknown" };
  return <span className={`risk-badge ${meta.color}`}>{meta.label}</span>;
}

function ResultCard({ result, onReset, role }) {
  const [apptStatus, setApptStatus] = useState("scheduled");
  const [statusLoading, setStatusLoading] = useState(null);

  const updateStatus = async (status) => {
    if (!result.appointment_id) return;
    setStatusLoading(status);
    try {
      const endpoint = status === "completed"
        ? `/appointments/${result.appointment_id}/complete`
        : `/appointments/${result.appointment_id}/cancel`;
      await api.put(endpoint);
      setApptStatus(status);
    } finally {
      setStatusLoading(null);
    }
  };

  const STATUS_META = {
    scheduled: { label: "Scheduled", color: "status-scheduled" },
    completed: { label: "Completed", color: "status-completed" },
    cancelled: { label: "Cancelled", color: "status-cancelled" },
  };
  return (
    <div className="result-card" role="region" aria-label="Assessment result">
      <div className="result-header">
        <h2 className="result-title">Assessment Complete</h2>
        <button className="btn-ghost" onClick={onReset} aria-label="Start new intake">
          New Intake
        </button>
      </div>

      <div className="result-grid">
        <div className="result-item">
          <span className="result-label">Risk Level</span>
          <RiskBadge level={result.risk_level} />
        </div>

        <div className="result-item">
          <span className="result-label">Specialty</span>
          <span className="result-value">{result.specialty ?? "—"}</span>
        </div>

        <div className="result-item full-width">
          <span className="result-label">Assigned Clinician</span>
          <span className="result-value clinician">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            {result.assigned_clinician ?? "Pending assignment"}
          </span>
        </div>

        {result.appointment_time && (
          <div className="result-item full-width">
            <span className="result-label">Appointment Time</span>
            <span className="result-value">
              {new Date(result.appointment_time).toLocaleString("en-GB", {
                day: "numeric",
                month: "short",
                year: "numeric",
                hour: "numeric",
                minute: "2-digit",
                hour12: true,
              })}
            </span>
          </div>
        )}

        {result.estimated_wait_minutes != null && (
          <div className="result-item full-width">
            <span className="result-label">Estimated Wait Time</span>
            <span className="result-value wait-time">
              {result.estimated_wait_minutes === 0
                ? "Available now"
                : result.estimated_wait_minutes < 60
                  ? `${result.estimated_wait_minutes} min`
                  : `${Math.floor(result.estimated_wait_minutes / 60)}h ${result.estimated_wait_minutes % 60}min`}
            </span>
          </div>
        )}

        {result.appointment_id && (
          <div className="result-item full-width">
            <span className="result-label">Appointment Status</span>
            <div className="status-row">
              <span className={`status-badge ${STATUS_META[apptStatus].color}`}>
                {STATUS_META[apptStatus].label}
              </span>
              <div className="status-actions">
                {role === "clinician" && (
                  <>
                    <button
                      className="btn-status completed"
                      disabled={apptStatus === "completed" || statusLoading != null}
                      onClick={() => updateStatus("completed")}
                    >
                      {statusLoading === "completed" ? "…" : "Mark Completed"}
                    </button>
                    <button
                      className="btn-status cancelled"
                      disabled={apptStatus === "cancelled" || statusLoading != null}
                      onClick={() => updateStatus("cancelled")}
                    >
                      {statusLoading === "cancelled" ? "…" : "Cancel"}
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {(result.risk_reasoning || result.specialty_reasoning) && (
        <div className="reasoning-section">
          <h3 className="reasoning-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            AI Reasoning
          </h3>

          {result.risk_reasoning && (
            <div className="reasoning-block">
              <span className="reasoning-label">Risk Assessment</span>
              <p className="reasoning-text">{result.risk_reasoning}</p>
            </div>
          )}

          {result.specialty_reasoning && (
            <div className="reasoning-block">
              <span className="reasoning-label">Specialty Recommendation</span>
              <p className="reasoning-text">{result.specialty_reasoning}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function HistoryPage() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/my-history")
      .then(({ data }) => setCases(data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="history-empty">Loading…</div>;
  if (!cases.length) return <div className="history-empty">No patient records yet.</div>;

  return (
    <div className="history-card">
      <h2 className="card-title">Patient History</h2>
      <p className="card-desc">{cases.length} record{cases.length !== 1 ? "s" : ""} found</p>
      <div className="history-table-wrapper">
        <table className="history-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Patient</th>
              <th>Age</th>
              <th>Symptoms</th>
              <th>Risk</th>
              <th>Specialty</th>
              <th>Clinician</th>
            </tr>
          </thead>
          <tbody>
            {cases.map((c) => (
              <tr key={c.id}>
                <td className="muted">{c.id}</td>
                <td><strong>{c.patient_name}</strong></td>
                <td>{c.age}</td>
                <td className="symptoms-cell">{c.symptoms}</td>
                <td><span className={`risk-badge risk-${c.risk_level?.toLowerCase()}`}>{c.risk_level}</span></td>
                <td>{c.specialty}</td>
                <td>{c.assigned_clinician}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function App() {
  const [fields, setFields] = useState({ name: sessionStorage.getItem("name") ?? "", age: "", symptoms: "", duration: "" });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState("intake");
  const [role, setRole] = useState(() => sessionStorage.getItem("role"));
  const [userName, setUserName] = useState(() => sessionStorage.getItem("name") ?? "");
  const [authed, setAuthed] = useState(() => !!sessionStorage.getItem("token"));

  const handleLogin = (userRole) => {
    setRole(userRole);
    setUserName(sessionStorage.getItem("name") ?? "");
    setAuthed(true);
  };

  const handleLogout = () => {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("role");
    sessionStorage.removeItem("name");
    setAuthed(false);
    setRole(null);
    setUserName("");
    setResult(null);
    setError(null);
  };

  const set = (key) => (e) => setFields((f) => ({ ...f, [key]: e.target.value }));
  const isValid = fields.name.trim() && fields.age.trim() && fields.symptoms.trim() && fields.duration.trim();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      setLoading(true);
      const intakeForm = `Name: ${fields.name}\nAge: ${fields.age}\nSymptoms: ${fields.symptoms}\nDuration: ${fields.duration}`;
      const { data } = await api.post("/intake", { intake_form: intakeForm });
      if (data.followup_message && !data.risk_level) {
        setError(data.followup_message);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError(err.response?.data?.detail ?? "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    setFields({ name: userName, age: "", symptoms: "", duration: "" });
  };

  if (!authed) return <LoginPage onLogin={handleLogin} />;

  const navItems = [
    { key: "intake", label: "Intake", roles: ["patient", "admin"] },
    { key: "history", label: "History", roles: ["patient", "admin"] },
    { key: "clinician", label: "My Patients", roles: ["clinician"] },
    { key: "admin", label: "Admin", roles: ["admin"] },
  ].filter((n) => n.roles.includes(role));

  return (
    <div className="app-wrapper">
      <header className="app-header">
        <div className="logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
        </div>
        <div>
          <h1 className="app-title">Telehealth AI Receptionist</h1>
          <p className="app-subtitle">{userName ? `Welcome, ${userName}` : "Secure, AI-powered patient intake"}</p>
        </div>
        <nav className="app-nav">
          {navItems.map((n) => (
            <button
              key={n.key}
              className={`nav-btn ${page === n.key ? "active" : ""}`}
              onClick={() => { setPage(n.key); setError(null); }}
            >{n.label}</button>
          ))}
          <button className="nav-btn nav-logout" onClick={handleLogout}>Sign Out</button>
        </nav>
      </header>

      <main className="app-main">
        {page === "history" && <HistoryPage />}
        {page === "clinician" && <ClinicianDashboard />}
        {page === "admin" && <AdminDashboard />}
        {page === "intake" && (
          result ? (
            <ResultCard result={result} onReset={handleReset} role={role} />
          ) : (
            <form className="intake-card" onSubmit={handleSubmit} noValidate>
              <h2 className="card-title">Patient Intake Form</h2>
              <p className="card-desc">Fill in your details and describe your symptoms to get started.</p>

              <div className="form-row">
                <div className="field">
                  <label htmlFor="name" className="field-label">Full Name</label>
                  <input id="name" className="field-input" type="text" placeholder="Jane Doe"
                    value={fields.name} onChange={set("name")} autoComplete="name" required />
                </div>
                <div className="field">
                  <label htmlFor="age" className="field-label">Age</label>
                  <input id="age" className="field-input" type="number" placeholder="32"
                    value={fields.age} onChange={set("age")} min="0" max="130" required />
                </div>
              </div>

              <div className="field">
                <label htmlFor="symptoms" className="field-label">Symptoms</label>
                <textarea id="symptoms" className="field-input field-textarea"
                  placeholder="Describe your symptoms in detail…"
                  value={fields.symptoms} onChange={set("symptoms")} rows={4} required />
              </div>

              <div className="field">
                <label htmlFor="duration" className="field-label">Duration</label>
                <input id="duration" className="field-input" type="text"
                  placeholder="e.g. 3 days, 2 weeks"
                  value={fields.duration} onChange={set("duration")} required />
              </div>

              {error && (
                <div className="error-banner" role="alert">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                    <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                  <div>
                    <strong>More information needed</strong>
                    <p style={{ margin: "4px 0 0", fontSize: "0.85rem" }}>{error}</p>
                  </div>
                </div>
              )}

              <button type="submit" className="btn-primary" disabled={loading || !isValid}>
                {loading ? <><span className="spinner" aria-hidden="true" />Analyzing…</> : "Submit Intake"}
              </button>
            </form>
          )
        )}
      </main>

      <footer className="app-footer">
        <p>This tool is for triage assistance only and does not replace professional medical advice.</p>
      </footer>
    </div>
  );
}

export default App;