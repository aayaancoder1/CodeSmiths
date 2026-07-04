import React from 'react';
import Button from '../../components/Buttons/Button';
import Input from '../../components/Inputs/Input';

const Login = () => {
  const handleSubmit = (e) => {
    e.preventDefault();
    // No auth implementation or logic, redirect would be handled here in the future
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-3xl font-extrabold text-white">Sign in to CodeSmiths</h2>
        <p className="mt-2 text-sm text-slate-400">
          Enter details below to access the interface
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input 
          label="Email Address" 
          type="email" 
          placeholder="name@company.com" 
          required 
        />
        <Input 
          label="Password" 
          type="password" 
          placeholder="••••••••" 
          required 
        />

        <div className="flex items-center justify-between text-sm">
          <label className="flex items-center text-slate-450">
            <input type="checkbox" className="rounded bg-slate-950 border-slate-800 text-brand-500 mr-2" />
            Remember me
          </label>
          <a href="#" className="font-medium text-brand-500 hover:text-brand-400 transition-colors">
            Forgot password?
          </a>
        </div>

        <Button type="submit" variant="primary" className="w-full mt-2">
          Sign In
        </Button>
      </form>
    </div>
  );
};

export default Login;
