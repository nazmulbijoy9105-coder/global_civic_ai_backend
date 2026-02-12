const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function registerUser({ email, password, consent }) {
  const res = await fetch(`${API_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ email, password, consent }),
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail || "Signup failed");
  }
  return res.json();
}

export async function loginUser({ email, password }) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    credentials: "include",
    body: new URLSearchParams({ username: email, password }),
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail || "Login failed");
  }
  return res.json();
}
