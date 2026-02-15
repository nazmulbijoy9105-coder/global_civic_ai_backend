const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
export async function getHealth(){return (await fetch(`${API_BASE}/health`)).json();}
export async function loginUser(credentials){return (await fetch(`${API_BASE}/login`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(credentials)})).json();}
export async function registerUser(data){return (await fetch(`${API_BASE}/register`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})).json();}
