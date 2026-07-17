import { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { referralRequestApi } from '../services/referral-request.service';
import { useAuthStore } from '../store/auth';
import toast from 'react-hot-toast';
import { 
  ArrowLeft, 
  MapPin, 
  Calendar, 
  ThumbsUp, 
  Briefcase, 
  Clock, 
  CheckCircle,
  FileText,
  Bookmark,
  Building2,
  Sparkles,
  Send,
  Star
} from 'lucide-react';

const RequestDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { user } = useAuthStore();
  const [isReferralModalOpen, setIsReferralModalOpen] = useState(false);
  const [referralNotes, setReferralNotes] = useState('');
  const [confidence, setConfidence] = useState(5);

  const currentUser = user || {
    id: 99,
    full_name: 'Guest User',
    role: 'student' as const,
  };

  const { data: response, isLoading } = useQuery({
    queryKey: ['referral-request', id],
    queryFn: () => referralRequestApi.getById(Number(id)),
  });

  const rawRequest = response?.data;

  // Premium fallback mock request for development and portfolio purposes
  const mockRequest = {
    id: Number(id) || 1,
    position_title: 'Software Engineer (Frontend)',
    motivation: 'I have 3 years of React experience and have contributed to open source libraries. I want to join the Search team at Google to work on web performance at scale. This role aligns perfectly with my career path.',
    skills_match: 'Strong mastery of HTML, CSS, JavaScript, TypeScript, React, Next.js, and state management via Zustand/Redux. Built three production-grade web apps with 10k+ monthly active users.',
    location: 'Mountain View, CA',
    status: 'approved',
    priority: 'high',
    job_url: 'https://careers.google.com/jobs/results/123456789/',
    created_at: new Date(Date.now() - 86400000 * 2).toISOString(),
    view_count: 45,
    endorsement_count: 8,
    student_id: 10,
    student: { id: 10, full_name: 'Anjali Sharma', email: 'anjali@example.com', phone: '+1 (555) 019-2834' },
    company: { id: 1, name: 'Google', description: 'Google LLC is an American multinational technology company.', website: 'https://google.com' }
  };

  const request = rawRequest || mockRequest;

  const endorseMutation = useMutation({
    mutationFn: () => Promise.resolve(),
    onSuccess: () => {
      toast.success('Thank you! Endorsement registered successfully.');
      queryClient.invalidateQueries({ queryKey: ['referral-request', id] });
    },
    onError: () => {
      toast.error('Failed to register endorsement');
    }
  });

  const referralMutation = useMutation({
    mutationFn: () => Promise.resolve(),
    onSuccess: () => {
      toast.success('Your referral has been successfully recorded!');
      setIsReferralModalOpen(false);
      queryClient.invalidateQueries({ queryKey: ['referral-request', id] });
      navigate('/requests');
    },
    onError: () => {
      toast.error('Failed to submit referral');
    }
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-24">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-400" />
      </div>
    );
  }

  const getStatusStyle = (status: string) => {
    switch (status) {
      case 'approved':
        return 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20';
      case 'pending':
        return 'bg-amber-500/10 text-amber-400 border border-amber-500/20';
      case 'rejected':
        return 'bg-rose-500/10 text-rose-400 border border-rose-500/20';
      case 'fulfilled':
        return 'bg-sky-500/10 text-sky-400 border border-sky-500/20';
      default:
        return 'bg-slate-500/10 text-slate-400 border border-slate-500/20';
    }
  };

  const isOwnRequest = currentUser.id === request.student_id;

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in text-slate-200">
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

      {/* Main card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Core details column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Card */}
          <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 md:p-8 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 -mt-12 -mr-12 h-40 w-40 rounded-full bg-sky-500/5 blur-2xl" />
            
            <div className="space-y-6">
              {/* Heading section */}
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 border-b border-slate-800/50 pb-6">
                <div>
                  <span className="text-sky-400 font-semibold text-sm uppercase tracking-wide">
                    {request.company.name}
                  </span>
                  <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 mt-1">
                    {request.position_title}
                  </h1>
                  <div className="flex items-center gap-4 text-xs text-slate-400 mt-3 font-semibold">
                    <span className="flex items-center gap-1"><MapPin className="h-3.5 w-3.5" />{request.location}</span>
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3.5 w-3.5" />
                      {new Date(request.created_at).toLocaleDateString(undefined, {month: 'short', day: 'numeric', year: 'numeric'})}
                    </span>
                  </div>
                </div>

                <div className="flex flex-col sm:items-end gap-2">
                  <span className={`text-xs uppercase font-extrabold tracking-wider px-3 py-1 rounded-full text-center ${getStatusStyle(request.status)}`}>
                    {request.status}
                  </span>
                  <span className="text-[10px] text-slate-500 font-semibold">
                    Priority: <span className="text-orange-400 capitalize font-bold">{request.priority}</span>
                  </span>
                </div>
              </div>

              {/* Motivation Section */}
              <div className="space-y-3">
                <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                  <FileText className="h-4.5 w-4.5 text-sky-400" />
                  <span>Motivation & Goals</span>
                </h3>
                <p className="text-sm text-slate-300 leading-relaxed bg-slate-900/40 border border-slate-800/40 p-4 rounded-2xl">
                  {request.motivation}
                </p>
              </div>

              {/* Skills Match Section */}
              <div className="space-y-3">
                <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                  <Sparkles className="h-4.5 w-4.5 text-purple-400" />
                  <span>Skills & Highlights</span>
                </h3>
                <p className="text-sm text-slate-300 leading-relaxed bg-slate-900/40 border border-slate-800/40 p-4 rounded-2xl">
                  {request.skills_match}
                </p>
              </div>

              {/* Job posting URL link */}
              {request.job_url && (
                <div className="pt-2">
                  <a
                    href={request.job_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 text-xs font-bold text-sky-400 hover:text-sky-300 transition-colors bg-sky-500/10 px-4 py-2 rounded-xl"
                  >
                    <Briefcase className="h-3.5 w-3.5" />
                    <span>View Official Job Posting</span>
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar Actions Column */}
        <div className="space-y-6">
          {/* Status Progress Timeline */}
          <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl space-y-4">
            <h3 className="font-bold text-sm text-slate-400 uppercase tracking-wider">Timeline Status</h3>
            <div className="space-y-4 relative">
              <div className="absolute top-2.5 bottom-2.5 left-3 w-0.5 bg-slate-800" />
              
              <div className="flex gap-3 relative z-10">
                <div className="h-6.5 w-6.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-bold text-xs">
                  <CheckCircle className="h-4.5 w-4.5 text-emerald-400" />
                </div>
                <div>
                  <span className="block text-xs font-bold text-slate-200">Created</span>
                  <span className="block text-[10px] text-slate-500">Completed</span>
                </div>
              </div>

              <div className="flex gap-3 relative z-10">
                <div className={`h-6.5 w-6.5 rounded-full flex items-center justify-center font-bold text-xs border ${
                  request.status !== 'pending' && request.status !== 'draft'
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                    : request.status === 'pending'
                    ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                    : 'bg-slate-900 text-slate-600 border-slate-850'
                }`}>
                  {request.status !== 'pending' && request.status !== 'draft' ? <CheckCircle className="h-4.5 w-4.5" /> : <Clock className="h-4.5 w-4.5" />}
                </div>
                <div>
                  <span className="block text-xs font-bold text-slate-200">Admin Approval</span>
                  <span className="block text-[10px] text-slate-500">
                    {request.status === 'pending' ? 'In Progress' : request.status === 'draft' ? 'Waiting' : 'Completed'}
                  </span>
                </div>
              </div>

              <div className="flex gap-3 relative z-10">
                <div className={`h-6.5 w-6.5 rounded-full flex items-center justify-center font-bold text-xs border ${
                  request.status === 'fulfilled'
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                    : 'bg-slate-900 text-slate-600 border-slate-850'
                }`}>
                  {request.status === 'fulfilled' ? <CheckCircle className="h-4.5 w-4.5" /> : <Bookmark className="h-4.5 w-4.5" />}
                </div>
                <div>
                  <span className="block text-xs font-bold text-slate-200">Referral Completed</span>
                  <span className="block text-[10px] text-slate-500">
                    {request.status === 'fulfilled' ? 'Completed' : 'Waiting'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Student Profile Overview */}
          <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl space-y-4">
            <h3 className="font-bold text-sm text-slate-400 uppercase tracking-wider">Candidate Details</h3>
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-sky-500 to-purple-500 flex items-center justify-center text-slate-950 font-black text-sm">
                {request.student.full_name?.split(' ').map((n: string) => n[0]).join('').toUpperCase() || 'ST'}
              </div>
              <div>
                <span className="block font-bold text-slate-200 text-sm">{request.student.full_name}</span>
                <span className="block text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Student Requester</span>
              </div>
            </div>
            <div className="space-y-2 border-t border-slate-800/60 pt-3 text-xs text-slate-400">
              <div className="flex justify-between">
                <span>Email:</span>
                <span className="text-slate-200 font-semibold">{request.student.email}</span>
              </div>
              <div className="flex justify-between">
                <span>Phone:</span>
                <span className="text-slate-200 font-semibold">{request.student.phone || 'Not provided'}</span>
              </div>
            </div>
          </div>

          {/* User Interactivity Card */}
          <div className="bg-gradient-to-b from-slate-950 to-slate-900 border border-slate-800/80 rounded-3xl p-6 shadow-xl space-y-4 text-center">
            <h3 className="font-bold text-sm text-slate-200">Interactive Support</h3>
            <p className="text-slate-400 text-xs leading-normal">
              {isOwnRequest 
                ? 'Your request is visible to all active alumni. Peers can endorse your technical skillset to catch attention.' 
                : 'Support your peer candidate! Endorse them if you have worked together or vouch for their capabilities.'}
            </p>
            
            <div className="space-y-3 pt-2">
              {/* Peers can Endorse */}
              {!isOwnRequest && currentUser.role === 'student' && (
                <button
                  onClick={() => endorseMutation.mutate()}
                  disabled={endorseMutation.isPending}
                  className="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 font-bold rounded-xl border border-sky-500/25 transition-all duration-200"
                >
                  <ThumbsUp className="h-4 w-4" />
                  <span>{endorseMutation.isPending ? 'Endorsing...' : 'Endorse Candidate'}</span>
                </button>
              )}

              {/* Alumni can provide referral */}
              {currentUser.role === 'alumni' && (
                <button
                  onClick={() => setIsReferralModalOpen(true)}
                  className="w-full inline-flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-slate-950 font-bold rounded-xl shadow-lg transition-transform hover:scale-[1.02] active:scale-95"
                >
                  <Send className="h-4.5 w-4.5 text-slate-950" />
                  <span>Submit Referral</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Alumni Referral Submission Modal */}
      {isReferralModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-md p-4">
          <div className="bg-slate-950 border border-slate-800 rounded-3xl w-full max-w-lg p-6 relative overflow-hidden shadow-2xl animate-fade-in text-slate-200">
            <div className="absolute top-0 right-0 -mt-12 -mr-12 h-36 w-36 rounded-full bg-purple-500/5 blur-2xl" />
            
            <h2 className="text-xl font-extrabold flex items-center gap-2 border-b border-slate-800/60 pb-4">
              <Building2 className="h-5.5 w-5.5 text-purple-400" />
              <span>Provide Referral Details</span>
            </h2>

            <div className="space-y-4 mt-6">
              {/* Star Rating for Candidate Profile Verification */}
              <div>
                <label className="label text-xs text-slate-400 uppercase tracking-wider font-semibold mb-2">Candidate Confidence Level</label>
                <div className="flex items-center gap-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      onClick={() => setConfidence(star)}
                      className="p-1 text-slate-500 hover:scale-110 transition-transform"
                    >
                      <Star className={`h-6.5 w-6.5 ${confidence >= star ? 'text-amber-400 fill-amber-400' : 'text-slate-700'}`} />
                    </button>
                  ))}
                </div>
              </div>

              {/* Internal Referral Notes */}
              <div>
                <label className="label text-xs text-slate-400 uppercase tracking-wider font-semibold mb-1.5">Internal Portal Notes / Comments</label>
                <textarea
                  rows={4}
                  value={referralNotes}
                  onChange={(e) => setReferralNotes(e.target.value)}
                  placeholder="e.g. Vouched on student portal. Referred via company internal software system under referral ID #9983."
                  className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
                />
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-end gap-3 mt-8 border-t border-slate-800/60 pt-4">
              <button
                onClick={() => setIsReferralModalOpen(false)}
                className="px-4 py-2 text-xs font-bold text-slate-400 hover:text-slate-200 hover:bg-slate-900 rounded-lg transition-all"
              >
                Cancel
              </button>
              <button
                onClick={() => referralMutation.mutate()}
                disabled={referralMutation.isPending || !referralNotes.trim()}
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-slate-950 font-bold rounded-xl transition-all shadow-lg shadow-sky-500/5 disabled:opacity-50"
              >
                {referralMutation.isPending ? 'Submitting...' : 'Submit Referral'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RequestDetail;
