import { useState, useEffect } from "react";
import api from "./api";

const STATUS_META = {
    scheduled: { label: "Scheduled", color: "status-scheduled" },
    completed: { label: "Completed", color: "status-completed" },
    cancelled: { label: "Cancelled", color: "status-cancelled" },
};

export function ClinicianDashboard() {
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [updating, setUpdating] = useState(null);

    useEffect(() => {
        api.get("/my-appointments")
            .then(({ data }) => setAppointments(data))
            .catch(() => setError("Failed to load appointments"))
            .finally(() => setLoading(false));
    }, []);

    const updateStatus = async (appointmentId, status) => {
        setUpdating(appointmentId + status);
        try {
            const endpoint = status === "completed"
                ? `/appointments/${appointmentId}/complete`
                : `/appointments/${appointmentId}/cancel`;
            await api.put(endpoint);
            setAppointments((prev) =>
                prev.map((a) => a.id === appointmentId ? { ...a, status } : a)
            );
        } finally {
            setUpdating(null);
        }
    };

    if (loading) return <div className="history-empty">Loading appointments…</div>;
    if (error) return <div className="history-empty">{error}</div>;

    return (
        <div className="dashboard-card">
            <h2 className="card-title">My Appointments</h2>
            <p className="card-desc">{appointments.length} appointment{appointments.length !== 1 ? "s" : ""}</p>

            {appointments.length === 0 ? (
                <div className="history-empty">No appointments assigned yet.</div>
            ) : (
                <div className="appt-list">
                    {appointments.map((appt, i) => (
                        <div key={i} className="appt-item">
                            <div className="appt-info">
                                <span className="appt-name">{appt.patient_name}</span>
                                <span className="appt-time">
                                    {appt.start_time
                                        ? new Date(appt.start_time).toLocaleString("en-GB", {
                                            day: "numeric", month: "short", year: "numeric",
                                            hour: "numeric", minute: "2-digit", hour12: true,
                                        })
                                        : "—"}
                                </span>
                            </div>
                            <div className="appt-actions">
                                <span className={`status-badge ${STATUS_META[appt.status]?.color ?? "status-scheduled"}`}>
                                    {STATUS_META[appt.status]?.label ?? appt.status}
                                </span>
                                {appt.status === "scheduled" && (
                                    <>
                                        <button
                                            className="btn-status completed"
                                            disabled={updating != null}
                                            onClick={() => updateStatus(appt.id, "completed")}
                                        >
                                            {updating === appt.id + "completed" ? "…" : "Complete"}
                                        </button>
                                        <button
                                            className="btn-status cancelled"
                                            disabled={updating != null}
                                            onClick={() => updateStatus(appt.id, "cancelled")}
                                        >
                                            {updating === appt.id + "cancelled" ? "…" : "Cancel"}
                                        </button>
                                    </>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
