#!/bin/bash
# Single-command deploy script for Render

# --- 1. Backend push ---
cd backend
git add .
git commit -m "Deploy-ready backend" || echo "No backend changes"
git push origin main

# --- 2. Frontend push and API fix ---
cd ../frontend

# Set production environment variable
echo "NEXT_PUBLIC_API_URL=https://global-civic-ai-backend.onrender.com" > .env.production

# Fix lib/api.js for Render deployment
cat > lib/api.js <<EOL
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

// Health check
export async function getHealth() {
  const res = await fetch(\`\${API_BASE}/health\`);
  return res.json();
}

// Login user
export async function loginUser(credentials) {
  const res = await fetch(\`\${API_BASE}/login\`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  return res.json();
}

// Register user
export async function registerUser(data) {
  const res = await fetch(\`\${API_BASE}/register\`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}
EOL

# Commit and push frontend changes
git add lib/api.js
git add .env.production -f
git commit -m "Deploy-ready frontend: API + env" || echo "No frontend changes"
git push origin main

echo "✅ Backend and frontend pushed. Ready for Render deployment."
