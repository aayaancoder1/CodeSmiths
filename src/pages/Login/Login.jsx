import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../../components/ui/Buttons/Button';
import Input from '../../components/ui/Inputs/Input';
import Checkbox from '../../components/ui/Inputs/Checkbox';
import Alert from '../../components/ui/Feedback/Alert';
import { useToast } from '../../context/ToastContext';

const Login = () => {
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Simulate login authentication
    setTimeout(() => {
      setLoading(false);
      if (email !== 'admin@codesmiths.ai') {
        setError('Invalid username or password. Try using "admin@codesmiths.ai".');
      } else {
        addToast({
          message: 'Welcome back!',
          description: 'Signed in successfully. Redirecting to dashboard...',
          variant: 'success'
        });
        // Use a short delay so the toast is visible before navigation
        setTimeout(() => navigate('/dashboard'), 500);
      }
    }, 1500);
  };

  return (
    <div className="space-y-6 w-full max-w-md mx-auto">
      {/* Brand Logo & Title */}
      <div className="text-center space-y-2">
        <div
          className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 text-2xl select-none mb-2"
          role="img"
          aria-label="CodeSmiths logo"
        >
          🛠️
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white font-sans">
          AI Company Brain
        </h1>
        <p className="text-sm text-ui-text-secondary leading-relaxed">
          Access your organization's unified knowledge graph
        </p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="danger" onClose={() => setError('')} role="alert" aria-live="assertive">
          {error}
        </Alert>
      )}

      {/* Login Form */}
      <form
        onSubmit={handleSubmit}
        className="space-y-5 bg-ui-surface/40 border border-ui-border p-6 rounded-2xl backdrop-blur-md"
        aria-label="Sign in form"
        noValidate
      >
        <Input
          id="email"
          label="Email Address"
          type="email"
          placeholder="name@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={loading}
          autoComplete="email"
          aria-required="true"
        />

        <Input
          id="password"
          label="Password"
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          disabled={loading}
          autoComplete="current-password"
          aria-required="true"
        />

        <div className="flex items-center justify-between text-xs">
          <Checkbox
            id="remember-me"
            label="Remember me"
            checked={rememberMe}
            onChange={(checked) => setRememberMe(checked)}
            disabled={loading}
          />
          <a
            href="#"
            className="font-semibold text-brand-400 hover:text-brand-300 transition-colors focus:outline-none focus-visible:ring-1 focus-visible:ring-brand-400/50 rounded"
            aria-label="Forgot your password?"
          >
            Forgot password?
          </a>
        </div>

        <Button
          type="submit"
          variant="primary"
          className="w-full mt-2"
          loading={loading}
          disabled={!email.trim() || !password.trim()}
          aria-label="Sign in to your account"
        >
          Sign In
        </Button>
      </form>

      {/* Demo hint */}
      <p className="text-center text-[11px] text-ui-text-tertiary">
        Demo credentials: <span className="font-mono text-ui-text-secondary">admin@codesmiths.ai</span>
      </p>
    </div>
  );
};

export default Login;
