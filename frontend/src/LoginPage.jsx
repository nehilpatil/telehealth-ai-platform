import { useState } from "react";
import api from "./api";

export function LoginPage({ onLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [showRegister, setShowRegister] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            const { data } = await api.post("/login", { email, password });
            if (!data.access_token) {
                setError(data.message ?? "Login failed");
                return;
            }
            sessionStorage.setItem("token", data.access_token);
            sessionStorage.setItem("role", data.role);
            sessionStorage.setItem("name", data.name ?? "");
            onLogin(data.role);
        } catch {
            setError("Invalid credentials");
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            await api.post("/register", { email, password, role: "patient", name });
            setShowRegister(false);
            setName("");
            setError(null);
        } catch {
            setError("Registration failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-wrapper">
            <div className="auth-card">
                <div className="auth-logo">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                    </svg>
                </div>
                <h1 className="auth-title">Telehealth AI</h1>
                <p className="auth-subtitle">{showRegister ? "Create a patient account" : "Sign in to continue"}</p>

                <form onSubmit={showRegister ? handleRegister : handleLogin} noValidate>
                    {showRegister && (
                        <div className="field">
                            <label htmlFor="name" className="field-label">Full Name</label>
                            <input id="name" className="field-input" type="text" placeholder="Jane Smith"
                                value={name} onChange={(e) => setName(e.target.value)} required />
                        </div>
                    )}
                    <div className="field">
                        <label htmlFor="email" className="field-label">Email</label>
                        <input id="email" className="field-input" type="email" placeholder="you@example.com"
                            value={email} onChange={(e) => setEmail(e.target.value)} required />
                    </div>
                    <div className="field">
                        <label htmlFor="password" className="field-label">Password</label>
                        <input id="password" className="field-input" type="password" placeholder="••••••••"
                            value={password} onChange={(e) => setPassword(e.target.value)} required />
                    </div>

                    {error && (
                        <div className="error-banner" role="alert">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                                <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
                            </svg>
                            {error}
                        </div>
                    )}

                    <button type="submit" className="btn-primary" disabled={loading || !email || !password || (showRegister && !name)}>
                        {loading ? <><span className="spinner" aria-hidden="true" /> Working…</> : showRegister ? "Create Account" : "Sign In"}
                    </button>
                </form>

                <p className="auth-toggle">
                    {showRegister ? "Already have an account?" : "New patient?"}{" "}
                    <button className="link-btn" onClick={() => { setShowRegister(!showRegister); setError(null); }}>
                        {showRegister ? "Sign in" : "Register"}
                    </button>
                </p>
            </div>
        </div>
    );
}
