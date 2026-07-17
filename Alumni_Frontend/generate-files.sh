#!/bin/bash

# Frontend File Generator Script
# This script creates all necessary files for the Alumni Referral Frontend

echo "Generating Alumni Referral Frontend Files..."

# Create directory structure
mkdir -p src/{layouts,pages/{auth,admin},components/{ui,forms},hooks,utils,assets}

# Create remaining core files
cat > src/layouts/AuthLayout.tsx << 'AUTHEOF'
import { ReactNode } from 'react';

interface AuthLayoutProps {
  children: ReactNode;
}

const AuthLayout = ({ children }: AuthLayoutProps) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-primary-600 mb-2">
            Alumni Referrals
          </h1>
          <p className="text-gray-600">
            Connect with alumni for career opportunities
          </p>
        </div>
        {children}
      </div>
    </div>
  );
};

export default AuthLayout;
AUTHEOF

echo "✓ Created AuthLayout"

# Create Login page
cat > src/pages/auth/Login.tsx << 'LOGINEOF'
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { authApi } from '@/services/auth.service';
import { useAuthStore } from '@/store/auth';
import { LogIn } from 'lucide-react';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

type LoginForm = z.infer<typeof loginSchema>;

const Login = () => {
  const navigate = useNavigate();
  const { setAuth } = useAuthStore();
  
  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  });

  const loginMutation = useMutation({
    mutationFn: (data: LoginForm) => authApi.login({ username: data.email, password: data.password }),
    onSuccess: async (response) => {
      const { access_token, refresh_token } = response.data;
      
      // Get user info (you'll need to add this endpoint to backend)
      // For now, decode from token or use stored data
      const user = JSON.parse(atob(access_token.split('.')[1]));
      
      setAuth(user, access_token, refresh_token);
      toast.success('Login successful!');
      navigate('/dashboard');
    },
    onError: () => {
      toast.error('Invalid credentials');
    },
  });

  const onSubmit = (data: LoginForm) => {
    loginMutation.mutate(data);
  };

  return (
    <div className="card">
      <div className="text-center mb-6">
        <LogIn className="mx-auto h-12 w-12 text-primary-600 mb-2" />
        <h2 className="text-2xl font-bold">Login</h2>
        <p className="text-gray-600 text-sm mt-1">Sign in to your account</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="label">Email</label>
          <input
            type="email"
            {...register('email')}
            className="input"
            placeholder="you@example.com"
          />
          {errors.email && (
            <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
          )}
        </div>

        <div>
          <label className="label">Password</label>
          <input
            type="password"
            {...register('password')}
            className="input"
            placeholder="••••••••"
          />
          {errors.password && (
            <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={loginMutation.isPending}
          className="btn-primary w-full"
        >
          {loginMutation.isPending ? 'Logging in...' : 'Login'}
        </button>
      </form>

      <p className="text-center text-sm text-gray-600 mt-4">
        Don't have an account?{' '}
        <Link to="/register" className="text-primary-600 hover:text-primary-700 font-medium">
          Register
        </Link>
      </p>
    </div>
  );
};

export default Login;
LOGINEOF

echo "✓ Created Login page"

# Create Register page (similar structure)
cat > src/pages/auth/Register.tsx << 'REGEOF'
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { authApi } from '@/services/auth.service';
import { UserPlus } from 'lucide-react';

const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  full_name: z.string().optional(),
  role: z.enum(['student', 'alumni']),
});

type RegisterForm = z.infer<typeof registerSchema>;

const Register = () => {
  const navigate = useNavigate();
  
  const { register, handleSubmit, formState: { errors } } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
    defaultValues: { role: 'student' },
  });

  const registerMutation = useMutation({
    mutationFn: authApi.register,
    onSuccess: () => {
      toast.success('Registration successful! Please login.');
      navigate('/login');
    },
    onError: () => {
      toast.error('Registration failed');
    },
  });

  return (
    <div className="card">
      <div className="text-center mb-6">
        <UserPlus className="mx-auto h-12 w-12 text-primary-600 mb-2" />
        <h2 className="text-2xl font-bold">Register</h2>
      </div>

      <form onSubmit={handleSubmit((data) => registerMutation.mutate(data))} className="space-y-4">
        <div>
          <label className="label">Email</label>
          <input {...register('email')} className="input" type="email" />
          {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>}
        </div>

        <div>
          <label className="label">Full Name</label>
          <input {...register('full_name')} className="input" />
        </div>

        <div>
          <label className="label">Password</label>
          <input {...register('password')} className="input" type="password" />
          {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>}
        </div>

        <div>
          <label className="label">I am a</label>
          <select {...register('role')} className="input">
            <option value="student">Student</option>
            <option value="alumni">Alumni</option>
          </select>
        </div>

        <button type="submit" disabled={registerMutation.isPending} className="btn-primary w-full">
          {registerMutation.isPending ? 'Registering...' : 'Register'}
        </button>
      </form>

      <p className="text-center text-sm text-gray-600 mt-4">
        Already have an account?{' '}
        <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
          Login
        </Link>
      </p>
    </div>
  );
};

export default Register;
REGEOF

echo "✓ Created Register page"

# Create placeholder pages
for page in Dashboard ReferralRequests CreateRequest RequestDetail Companies Profile; do
  cat > "src/pages/${page}.tsx" << PAGEEOF
const ${page} = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">${page}</h1>
      <div className="card">
        <p>Implement ${page} component here</p>
      </div>
    </div>
  );
};

export default ${page};
PAGEEOF
  echo "✓ Created ${page} page"
done

# Create admin panel
cat > src/pages/admin/AdminPanel.tsx << 'ADMINEOF'
const AdminPanel = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Admin Panel</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="font-semibold mb-2">Pending Requests</h3>
          <p className="text-3xl font-bold text-primary-600">12</p>
        </div>
        <div className="card">
          <h3 className="font-semibold mb-2">Total Users</h3>
          <p className="text-3xl font-bold text-primary-600">245</p>
        </div>
        <div className="card">
          <h3 className="font-semibold mb-2">Active Companies</h3>
          <p className="text-3xl font-bold text-primary-600">58</p>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
ADMINEOF

echo "✓ Created AdminPanel"

# Create .env.example
cat > .env.example << 'ENVEOF'
VITE_API_URL=http://localhost:8000/api/v1
ENVEOF

echo "✓ Created .env.example"

# Create .gitignore
cat > .gitignore << 'GITEOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Production
dist/
build/

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Editor
.vscode/
.idea/

# Env
.env
GITEOF

echo "✓ Created .gitignore"

echo ""
echo "Frontend file generation complete!"
echo "Next steps:"
echo "1. cd Alumni_Frontend"
echo "2. npm install"
echo "3. cp .env.example .env"
echo "4. npm run dev"
