import { useState, useEffect } from "react";
import api from "./api";

const ROLE_COLOR = {
    admin: "risk-high",
    clinician: "risk-medium",
    patient: "risk-low",
};

export function AdminDashboard() {
    const [users, setUsers] = useState([]);
    const [appointments, setAppointments] = useState([]);
    const [cases, setCases] = useState([]);
    const [tab, setTab] = useState("users");
    const [loading, setLoading] = useState(true);
    const [clinForm, setClinForm] = useState({ name: "", email: "", password: "", specialty: "" });
    const [clinLoading, setClinLoading] = useState(false);
    const [clinMsg, setClinMsg] = useState(null);

    useEffect(() => {
        Promise.all([
            api.get("/users"),
            api.get("/appointments"),
            api.get("/patients"),
        ]).then(([u, a, p]) => {
            setUsers(u.data);
            setAppointments(a.data);
            setCases(p.data);
        }).catch(() => {
            setUsers([]);
            setAppointments([]);
            setCases([]);
        }).finally(() => setLoading(false));
    }, []);

    const handleCreateClinician = async (e) => {
        e.preventDefault();
        setClinLoading(true);
        setClinMsg(null);
        try {
            const { data } = await api.post("/admin/create-clinician", clinForm);
            if (data.success) {
                setClinMsg({ ok: true, text: "Clinician created successfully." });
                setClinForm({ name: "", email: "", password: "", specialty: "" });
            } else {
                setClinMsg({ ok: false, text: data.message ?? "Failed to create clinician." });
            }
        } catch {
            setClinMsg({ ok: false, text: "Request failed." });
        } finally {
            setClinLoading(false);
        }
    };

    if (loading) return <div className="history-empty">Loading…</div>;

    return (
        <div className="dashboard-card">
            <h2 className="card-title">Admin Dashboard</h2>

            <div className="dash-tabs">
                <button className={`nav-btn ${tab === "users" ? "active" : ""}`} onClick={() => setTab("users")}>
                    Users ({users.length})
                </button>
                <button className={`nav-btn ${tab === "appointments" ? "active" : ""}`} onClick={() => setTab("appointments")}>
                    Appointments ({appointments.length})
                </button>
                <button className={`nav-btn ${tab === "history" ? "active" : ""}`} onClick={() => setTab("history")}>
                    Patient History ({cases.length})
                </button>
                <button className={`nav-btn ${tab === "create-clinician" ? "active" : ""}`} onClick={() => setTab("create-clinician")}>
                    Create Clinician
                </button>
            </div>

            {tab === "users" && (
                <div className="history-table-wrapper">
                    <table className="history-table">
                        <thead>
                            <tr><th>#</th><th>Email</th><th>Role</th></tr>
                        </thead>
                        <tbody>
                            {users.map((u) => (
                                <tr key={u.id}>
                                    <td className="muted">{u.id}</td>
                                    <td>{u.email}</td>
                                    <td><span className={`risk-badge ${ROLE_COLOR[u.role] ?? "risk-unknown"}`}>{u.role}</span></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {tab === "appointments" && (
                <div className="history-table-wrapper">
                    <table className="history-table">
                        <thead>
                            <tr><th>#</th><th>Patient</th><th>Clinician</th><th>Time</th><th>Status</th></tr>
                        </thead>
                        <tbody>
                            {appointments.map((a) => (
                                <tr key={a.id}>
                                    <td className="muted">{a.id}</td>
                                    <td>{a.patient_name}</td>
                                    <td>{users.find((u) => u.id === a.clinician_id)?.name ?? `Clinician #${a.clinician_id}`}</td>
                                    <td>{a.start_time ? new Date(a.start_time).toLocaleString("en-GB", {
                                        day: "numeric", month: "short", hour: "numeric", minute: "2-digit", hour12: true,
                                    }) : "—"}</td>
                                    <td>
                                        <span className={`status-badge status-${a.status}`}>{a.status}</span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {tab === "history" && (
                cases.length === 0
                    ? <div className="history-empty">No patient records yet.</div>
                    : <div className="history-table-wrapper">
                        <table className="history-table">
                            <thead>
                                <tr><th>#</th><th>Patient</th><th>Age</th><th>Symptoms</th><th>Risk</th><th>Specialty</th><th>Assigned Doctor</th></tr>
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
                                        <td>{c.assigned_clinician ?? "—"}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
            )}

            {tab === "create-clinician" && (
                <form className="intake-card" onSubmit={handleCreateClinician} noValidate style={{ boxShadow: "none", padding: "1.5rem 0 0" }}>
                    <p className="card-desc">Create a new clinician account and assign their specialty.</p>
                    {clinMsg && (
                        <div className={clinMsg.ok ? "success-banner" : "error-banner"} role="alert">{clinMsg.text}</div>
                    )}
                    <div className="form-row">
                        <div className="field">
                            <label className="field-label">Full Name</label>
                            <input className="field-input" type="text" placeholder="Dr. Jane Smith" required
                                value={clinForm.name} onChange={(e) => setClinForm((f) => ({ ...f, name: e.target.value }))} />
                        </div>
                        <div className="field">
                            <label className="field-label">Email</label>
                            <input className="field-input" type="email" placeholder="dr.jane@clinic.com" required
                                value={clinForm.email} onChange={(e) => setClinForm((f) => ({ ...f, email: e.target.value }))} />
                        </div>
                    </div>
                    <div className="form-row">
                        <div className="field">
                            <label className="field-label">Password</label>
                            <input className="field-input" type="password" placeholder="••••••••" required
                                value={clinForm.password} onChange={(e) => setClinForm((f) => ({ ...f, password: e.target.value }))} />
                        </div>
                        <div className="field">
                            <label className="field-label">Specialty</label>
                            <input className="field-input" type="text" placeholder="e.g. Cardiology" required
                                value={clinForm.specialty} onChange={(e) => setClinForm((f) => ({ ...f, specialty: e.target.value }))} />
                        </div>
                    </div>
                    <button type="submit" className="btn-primary"
                        disabled={clinLoading || !clinForm.name || !clinForm.email || !clinForm.password || !clinForm.specialty}>
                        {clinLoading ? "Creating…" : "Create Clinician"}
                    </button>
                </form>
            )}
        </div>
    );
}
