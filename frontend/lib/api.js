const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function fetchJson(url, options = {}) {
  const res = await fetch(url, options);
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

export async function registerUser({ username, email, password }) {
  return fetchJson(API_URL + "/auth/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });
}

export async function loginUser({ email, password }) {
  return fetchJson(API_URL + "/auth/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
}

export async function getAssessment() {
  return fetchJson(API_URL + "/questions/assessment");
}

export async function getRandomQuestion() {
  return fetchJson(API_URL + "/questions/random");
}

export async function checkHealth() {
  return fetchJson(API_URL + "/health");
}
