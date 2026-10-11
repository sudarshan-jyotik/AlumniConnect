import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { GoogleLogin } from '@react-oauth/google';
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

  const handleAuthSuccess = async (access_token: string, refresh_token: string, emailFallback?: string) => {
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    
    try {
      const userResponse = await authApi.getCurrentUser();
      const fullUser = userResponse.data;
      setAuth(fullUser, access_token, refresh_token);
    } catch (err) {
      const decodedUser = JSON.parse(atob(access_token.split('.')[1]));
      const fallbackUser = {
        id: decodedUser.user_id,
        email: decodedUser.email || emailFallback || 'user@example.com',
        full_name: decodedUser.full_name || 'Alumni User',
        phone: null,
        role: decodedUser.role || 'student',
        status: 'active',
        is_email_verified: true,
        created_at: new Date().toISOString()
      };
      setAuth(fallbackUser as any, access_token, refresh_token);
    }
    
    toast.success('Login successful!');
    navigate('/dashboard');
  };

  const loginMutation = useMutation({
    mutationFn: (data: LoginForm) => authApi.login({ username: data.email, password: data.password }),
    onSuccess: async (response, variables) => {
      const { access_token, refresh_token } = response.data;
      await handleAuthSuccess(access_token, refresh_token, variables.email);
    },
    onError: () => {
      toast.error('Invalid credentials');
    },
  });

  const googleMutation = useMutation({
    mutationFn: (credential: string) => authApi.loginWithGoogle(credential),
    onSuccess: async (response) => {
      const { access_token, refresh_token } = response.data;
      await handleAuthSuccess(access_token, refresh_token);
    },
    onError: (err: any) => {
      toast.error(err?.response?.data?.detail || 'Google sign-in failed');
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

      <div className="my-5 flex items-center">
        <div className="flex-1 border-t border-slate-750" />
        <span className="px-3 text-xs text-slate-400 font-semibold uppercase">Or continue with</span>
        <div className="flex-1 border-t border-slate-750" />
      </div>

      {/* Google OAuth Login Button */}
      <div className="flex justify-center">
        <GoogleLogin
          onSuccess={(credentialResponse) => {
            if (credentialResponse.credential) {
              googleMutation.mutate(credentialResponse.credential);
            }
          }}
          onError={() => {
            toast.error('Google Sign-In was cancelled or failed');
          }}
          theme="filled_black"
          shape="pill"
          size="large"
          text="signin_with"
        />
      </div>

      <p className="text-center text-sm text-gray-600 mt-5">
        Don't have an account?{' '}
        <Link to="/register" className="text-primary-600 hover:text-primary-700 font-medium">
          Register
        </Link>
      </p>
    </div>
  );
};

export default Login;
