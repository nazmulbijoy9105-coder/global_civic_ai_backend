const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

// Health check
export async function getHealth() { const res = await fetch(`${API_BASE}/health`); return res.json(); }

// Login user
export async function loginUser(credentials) { const res = await fetch(`${API_BASE}/login`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(credentials) }); return res.json(); }

// Register user
export async function registerUser(data) { const res = await fetch(`${API_BASE}/register`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) }); return res.json(); }
