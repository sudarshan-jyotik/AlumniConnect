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
    onError: (err: any) => {
      const detail = err?.response?.data?.detail;
      if (Array.isArray(detail)) {
        toast.error(detail[0]?.msg || 'Registration failed');
      } else if (typeof detail === 'string') {
        toast.error(detail);
      } else {
        toast.error('Registration failed');
      }
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
          <input {...register('password')} className="input" type="password" placeholder="e.g. Pass1234" />
          <p className="text-xs text-gray-400 mt-1">Min 8 chars, 1 uppercase, 1 lowercase, 1 number</p>
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
