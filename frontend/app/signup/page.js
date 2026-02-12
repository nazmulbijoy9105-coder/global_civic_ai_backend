'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [consent, setConsent] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!consent) {
      setError('You must agree to the terms and privacy policy');
      return;
    }

    try {
      const data = await api.signup({ email, password, consent });
      setSuccess('Signup successful! Redirecting...');
      router.push('/dashboard');
    } catch (err) {
      setError(err.message || 'Signup failed');
    }
  };

  return (
    <main>
      <h1>Signup</h1>
      <form onSubmit={handleSubmit}>
        <label>Email:</label><br />
        <input
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        /><br />
        <label>Password:</label><br />
        <input
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        /><br />
        <label>
          <input
            type="checkbox"
            checked={consent}
            onChange={e => setConsent(e.target.checked)}
          />
          I agree to the terms and privacy policy
        </label><br /><br />
        <button type="submit">Sign Up</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
    </main>
  );
}
