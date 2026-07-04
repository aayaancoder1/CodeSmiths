import React, { useState } from 'react';
import Button from '../../components/ui/Buttons/Button';
import Input from '../../components/ui/Inputs/Input';
import Checkbox from '../../components/ui/Inputs/Checkbox';
import Alert from '../../components/ui/Feedback/Alert';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Simulate login loader
    setTimeout(() => {
      setLoading(false);
      // Simulating a dummy credential validation error for user testing demo
      if (email !== 'admin@codesmiths.ai') {
        setError('Invalid username or password. Try using "admin@codesmiths.ai".');
      } else {
        // Redirect to dashboard
        window.location.href = '/dashboard';
      }
    }, 1500);
  };

  return (
    <div className="space-y-6 w-full max-w-md mx-auto">
      {/* Brand Logo & Title */}
      <div className="text-center space-y-2">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 text-2xl select-none mb-2">
          🛠️
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-white font-sans">
          AI Company Brain
        </h2>
        <p className="text-sm text-ui-text-secondary leading-relaxed">
          Access your organization's unified knowledge graph
        </p>
      </div>

      {/* Error placeholder */}
      {error && (
        <Alert variant="danger" onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* Login Form */}
      <form onSubmit={handleSubmit} className="space-y-5 bg-ui-surface/40 border border-ui-border p-6 rounded-2xl backdrop-blur-md">
        <Input 
          label="Email Address" 
          type="email" 
          placeholder="name@company.com" 
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required 
          disabled={loading}
        />
        
        <Input 
          label="Password" 
          type="password" 
          placeholder="••••••••" 
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required 
          disabled={loading}
        />

        <div className="flex items-center justify-between text-xs">
          <Checkbox
            label="Remember me"
            checked={rememberMe}
            onChange={(checked) => setRememberMe(checked)}
            disabled={loading}
          />
          <a href="#" className="font-semibold text-brand-400 hover:text-brand-300 transition-colors">
            Forgot password?
          </a>
        </div>

        <Button 
          type="submit" 
          variant="primary" 
          className="w-full mt-2"
          loading={loading}
        >
          Sign In
        </Button>
      </form>
    </div>
  );
};

export default Login;
