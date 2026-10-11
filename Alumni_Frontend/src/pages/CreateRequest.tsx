import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { referralRequestApi } from '../services/referral-request.service';
import { companyApi } from '../services/company.service';
import { ArrowLeft, Send, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

const requestSchema = z.object({
  company_id: z.string().min(1, 'Please select a company'),
  position_title: z.string().min(2, 'Position title must be at least 2 characters'),
  job_url: z.string().url('Please enter a valid URL').or(z.literal('')),
  location: z.string().min(2, 'Location is required'),
  priority: z.enum(['low', 'medium', 'high', 'urgent']),
  motivation: z.string().min(20, 'Please explain your motivation in at least 20 characters'),
  skills_match: z.string().min(10, 'Please state your skills in at least 10 characters'),
});

type RequestForm = z.infer<typeof requestSchema>;

const CreateRequest = () => {
  const navigate = useNavigate();

  // Fetch companies list for selection
  const { data: companiesData } = useQuery({
    queryKey: ['companies-dropdown'],
    queryFn: () => companyApi.getAll(),
  });

  const rawCompanies = companiesData?.data || [];

  const companies = rawCompanies;

  const { register, handleSubmit, formState: { errors } } = useForm<RequestForm>({
    resolver: zodResolver(requestSchema),
    defaultValues: {
      priority: 'medium',
      job_url: '',
    }
  });

  const createRequestMutation = useMutation({
    mutationFn: (data: RequestForm) => referralRequestApi.create({
      company_id: Number(data.company_id),
      position_title: data.position_title,
      job_url: data.job_url || undefined,
      location: data.location,
      priority: data.priority,
      motivation: data.motivation,
      skills_match: data.skills_match,
    }),
    onSuccess: () => {
      toast.success('Referral request submitted for admin review!');
      navigate('/requests');
    },
    onError: () => {
      toast.error('Failed to submit request');
    }
  });

  const onSubmit = (data: RequestForm) => {
    createRequestMutation.mutate(data);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-fade-in text-slate-200">
      {/* Back button */}
      <div>
        <Link 
          to="/requests" 
          className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Requests</span>
        </Link>
      </div>

      {/* Header */}
      <div>
        <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">Request a Referral</h1>
        <p className="text-slate-500 text-xs mt-0.5">Let verified alumni know which open role you want a referral for</p>
      </div>

      {/* Form Card */}
      <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 md:p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 h-40 w-40 rounded-full bg-sky-500/5 blur-2xl" />
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Company selection */}
            <div>
              <label className="label text-slate-300">Company</label>
              <select 
                {...register('company_id')}
                className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
              >
                <option value="">Select a company...</option>
                {companies.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
              {errors.company_id && (
                <p className="text-rose-500 text-xs mt-1.5 font-semibold">{errors.company_id.message}</p>
              )}
            </div>

            {/* Position Title */}
            <div>
              <label className="label text-slate-300">Position Title</label>
              <input
                type="text"
                placeholder="e.g. Software Engineer (L3)"
                {...register('position_title')}
                className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
              />
              {errors.position_title && (
                <p className="text-rose-500 text-xs mt-1.5 font-semibold">{errors.position_title.message}</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Job URL */}
            <div>
              <label className="label text-slate-300">Job Posting URL (Optional)</label>
              <input
                type="text"
                placeholder="e.g. https://careers.google.com/jobs/..."
                {...register('job_url')}
                className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
              />
              {errors.job_url && (
                <p className="text-rose-500 text-xs mt-1.5 font-semibold">{errors.job_url.message}</p>
              )}
            </div>

            {/* Location */}
            <div>
              <label className="label text-slate-300">Job Location</label>
              <input
                type="text"
                placeholder="e.g. Cupertino, CA / Bengaluru / Remote"
                {...register('location')}
                className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
              />
              {errors.location && (
                <p className="text-rose-500 text-xs mt-1.5 font-semibold">{errors.location.message}</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Priority selection */}
            <div>
              <label className="label text-slate-300">Urgency Level</label>
              <select 
                {...register('priority')}
                className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
              >
                <option value="low">Low (General Application)</option>
                <option value="medium">Medium (Regular Application)</option>
                <option value="high">High (Closes soon / Highly Desired)</option>
                <option value="urgent">Urgent (Immediate Deadline)</option>
              </select>
              {errors.priority && (
                <p className="text-rose-500 text-xs mt-1.5 font-semibold">{errors.priority.message}</p>
              )}
            </div>
          </div>

          {/* Motivation textarea */}
          <div>
            <label className="label text-slate-300">Why are you interested in this role and company?</label>
            <textarea
              rows={4}
              placeholder="Vividly explain why you want to work here. What projects/initiatives excite you? Keep it personalized and professional."
              {...register('motivation')}
              className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
            />
            {errors.motivation && (
              <p className="text-rose-500 text-xs mt-1.5 font-semibold">{errors.motivation.message}</p>
            )}
          </div>

          {/* Skills Match */}
          <div>
            <label className="label text-slate-300 flex items-center gap-1.5">
              <span>How do your skills align with this position?</span>
              <span className="inline-flex items-center text-[10px] text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded-full font-bold">
                <Sparkles className="h-3 w-3 mr-1" />
                Resume Highlights
              </span>
            </label>
            <textarea
              rows={4}
              placeholder="Detail your technical languages, frame-works, certifications, or past internships that directly align with this role's description."
              {...register('skills_match')}
              className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
            />
            {errors.skills_match && (
              <p className="text-rose-500 text-xs mt-1.5 font-semibold">{errors.skills_match.message}</p>
            )}
          </div>

          {/* Submit Button */}
          <div className="flex items-center justify-end pt-4">
            <button
              type="submit"
              disabled={createRequestMutation.isPending}
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-slate-950 font-bold rounded-xl shadow-xl transition-all duration-200 hover:scale-[1.02] active:scale-95 disabled:opacity-50"
            >
              {createRequestMutation.isPending ? (
                <span>Submitting...</span>
              ) : (
                <>
                  <Send className="h-4.5 w-4.5 text-slate-950" />
                  <span>Submit Request</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateRequest;
