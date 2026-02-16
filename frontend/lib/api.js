const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

// Health check
export async function getHealth() {
  return (await fetch(`${API_BASE}/health`)).json();
}

// Login
export async function loginUser(credentials) {
  return (
    await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    })
  ).json();
}

// Signup
export async function registerUser(data) {
  return (
    await fetch(`${API_BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
  ).json();
}

// Current user
export async function getCurrentUser() {
  return (await fetch(`${API_BASE}/auth/me`)).json();
}
