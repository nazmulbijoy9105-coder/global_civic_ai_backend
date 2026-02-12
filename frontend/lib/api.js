const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const api = {
  getCurrentUser: async () => {
    const res = await fetch(`${API_URL}/auth/me`, {
      credentials: "include",
    });
    if (!res.ok) throw new Error("Not authenticated");
    return res.json();
  },

  login: async ({ email, password }) => {
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
  },

  signup: async ({ email, password, consent }) => {
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
  },

  logout: async () => {
    const res = await fetch(`${API_URL}/auth/logout`, {
      method: "POST",
      credentials: "include",
    });
    if (!res.ok) throw new Error("Logout failed");
    return res.json();
  },
};

