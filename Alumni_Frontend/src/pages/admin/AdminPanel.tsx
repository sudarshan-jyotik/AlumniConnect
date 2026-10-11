import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminApi } from '../../services/admin.service';
import toast from 'react-hot-toast';
import { 
  ShieldAlert, 
  Check, 
  X, 
  Building2, 
  User as UserIcon, 
  Calendar, 
  HelpCircle,
  Clock,
  Sparkles,
  Search,
  MessageSquare,
  GraduationCap,
  ExternalLink,
  BadgeCheck
} from 'lucide-react';

const AdminPanel = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<'requests' | 'alumni'>('requests');
  const [searchTerm, setSearchTerm] = useState('');
  const [isRejectModalOpen, setIsRejectModalOpen] = useState(false);
  const [selectedRequestId, setSelectedRequestId] = useState<number | null>(null);
  const [rejectReason, setRejectReason] = useState('');

  // 1. Real Stats
  const { data: statsResponse } = useQuery({
    queryKey: ['admin-real-stats'],
    queryFn: () => adminApi.getStats(),
  });
  const stats = statsResponse?.data;

  // 2. Real Pending Requests (No fallback mock)
  const { data: pendingResponse, isLoading: isLoadingRequests } = useQuery({
    queryKey: ['pending-requests'],
    queryFn: () => adminApi.getPendingRequests(),
  });
  const pendingRequests = pendingResponse?.data || [];

  // 3. Real Alumni Verifications Queue
  const { data: verificationsResponse, isLoading: isLoadingAlumni } = useQuery({
    queryKey: ['alumni-verifications'],
    queryFn: () => adminApi.getAlumniVerifications(),
  });
  const alumniList = verificationsResponse?.data || [];

  const approveMutation = useMutation({
    mutationFn: (id: number) => adminApi.approveRequest(id),
    onSuccess: () => {
      toast.success('Referral request successfully approved!');
      queryClient.invalidateQueries({ queryKey: ['pending-requests'] });
      queryClient.invalidateQueries({ queryKey: ['admin-real-stats'] });
    },
    onError: () => {
      toast.error('Failed to approve referral request');
    }
  });

  const rejectMutation = useMutation({
    mutationFn: (data: { id: number; reason: string }) => adminApi.rejectRequest(data.id, data.reason),
    onSuccess: () => {
      toast.success('Referral request rejected with feedback.');
      setIsRejectModalOpen(false);
      setRejectReason('');
      setSelectedRequestId(null);
      queryClient.invalidateQueries({ queryKey: ['pending-requests'] });
      queryClient.invalidateQueries({ queryKey: ['admin-real-stats'] });
    },
    onError: () => {
      toast.error('Failed to reject referral request');
    }
  });

  const verifyAlumniMutation = useMutation({
    mutationFn: (userId: number) => adminApi.verifyAlumni(userId),
    onSuccess: () => {
      toast.success('Alumni credentials verified!');
      queryClient.invalidateQueries({ queryKey: ['alumni-verifications'] });
      queryClient.invalidateQueries({ queryKey: ['admin-real-stats'] });
    },
    onError: () => {
      toast.error('Failed to verify alumni profile');
    }
  });

  const rejectAlumniMutation = useMutation({
    mutationFn: (userId: number) => adminApi.rejectAlumni(userId),
    onSuccess: () => {
      toast.success('Alumni verification rejected.');
      queryClient.invalidateQueries({ queryKey: ['alumni-verifications'] });
      queryClient.invalidateQueries({ queryKey: ['admin-real-stats'] });
    },
    onError: () => {
      toast.error('Failed to update alumni status');
    }
  });

  const handleApprove = (id: number) => {
    approveMutation.mutate(id);
  };

  const handleOpenRejectModal = (id: number) => {
    setSelectedRequestId(id);
    setIsRejectModalOpen(true);
  };

  const handleRejectSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRequestId) return;
    if (!rejectReason.trim()) {
      toast.error('Please provide a reason for rejection');
      return;
    }
    rejectMutation.mutate({ id: selectedRequestId, reason: rejectReason });
  };

  const filteredPending = pendingRequests.filter((req) => {
    return req.position_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
           (req.company?.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
           (req.student?.full_name || '').toLowerCase().includes(searchTerm.toLowerCase());
  });

  const filteredAlumni = alumniList.filter((a) => {
    return (a.user_name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
           (a.current_company_name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
           a.user_email.toLowerCase().includes(searchTerm.toLowerCase());
  });

  return (
    <div className="space-y-6 animate-fade-in text-slate-200">
      {/* Real Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-950 border border-slate-800/80 p-5 rounded-2xl flex items-center justify-between shadow">
          <div className="space-y-1">
            <span className="text-slate-500 text-xs font-bold uppercase tracking-wider">Pending Review Queue</span>
            <h3 className="text-3xl font-black text-slate-200">
              {stats ? stats.pending_requests_count : pendingRequests.length}
            </h3>
          </div>
          <div className="p-3 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-xl">
            <Clock className="h-6 w-6" />
          </div>
        </div>

        <div className="bg-slate-950 border border-slate-800/80 p-5 rounded-2xl flex items-center justify-between shadow">
          <div className="space-y-1">
            <span className="text-slate-500 text-xs font-bold uppercase tracking-wider">Unverified Alumni</span>
            <h3 className="text-3xl font-black text-slate-200">
              {stats ? stats.unverified_alumni_count : alumniList.filter(a => !a.is_verified).length}
            </h3>
          </div>
          <div className="p-3 bg-sky-500/10 text-sky-400 border border-sky-500/20 rounded-xl">
            <Sparkles className="h-6 w-6" />
          </div>
        </div>

        <div className="bg-slate-950 border border-slate-800/80 p-5 rounded-2xl flex items-center justify-between shadow">
          <div className="space-y-1">
            <span className="text-slate-500 text-xs font-bold uppercase tracking-wider">Approval Rate</span>
            <h3 className="text-3xl font-black text-slate-200">
              {stats ? `${stats.approval_rate_percentage}%` : '100%'}
            </h3>
          </div>
          <div className="p-3 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-xl">
            <Check className="h-6 w-6" />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800/80 gap-4">
        <button
          onClick={() => setActiveTab('requests')}
          className={`flex items-center gap-2 px-4 py-3 text-xs font-bold transition-all ${
            activeTab === 'requests' 
              ? 'text-sky-400 border-b-2 border-sky-400' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Clock className="h-4 w-4" />
          <span>Pending Student Requests ({pendingRequests.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('alumni')}
          className={`flex items-center gap-2 px-4 py-3 text-xs font-bold transition-all ${
            activeTab === 'alumni' 
              ? 'text-sky-400 border-b-2 border-sky-400' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <GraduationCap className="h-4 w-4" />
          <span>Alumni Identity Verifications ({alumniList.length})</span>
        </button>
      </div>

      {/* Section 1: Referral Requests */}
      {activeTab === 'requests' && (
        <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-slate-200">Pending Student Referral Requests</h2>
              <p className="text-slate-500 text-xs mt-0.5">Vouch for academic quality before releasing requests to alumni</p>
            </div>

            <div className="relative w-full sm:w-72">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
              <input
                type="text"
                placeholder="Search requests..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2 pl-9 pr-3 text-xs text-slate-200 focus:outline-none placeholder-slate-500"
              />
            </div>
          </div>

          {isLoadingRequests ? (
            <div className="flex justify-center items-center py-16">
              <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-sky-400" />
            </div>
          ) : filteredPending.length === 0 ? (
            <div className="p-12 text-center">
              <HelpCircle className="h-10 w-10 text-slate-600 mx-auto mb-3" />
              <h4 className="font-bold text-slate-400 text-sm">Review Queue is Completely Clear</h4>
              <p className="text-slate-600 text-xs mt-0.5">All student requests are currently processed!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredPending.map((req) => (
                <div 
                  key={req.id}
                  className="border border-slate-850 hover:border-slate-800 bg-slate-900/10 p-5 rounded-2xl transition-all flex flex-col md:flex-row md:items-start justify-between gap-4"
                >
                  <div className="space-y-3 flex-1">
                    <div className="flex flex-wrap items-center gap-3">
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded">
                        <Building2 className="h-3 w-3" />
                        <span>{req.company?.name || 'Company'}</span>
                      </span>
                      <h4 className="font-extrabold text-sm text-slate-200">{req.position_title}</h4>
                      <span className="text-[10px] text-orange-400 font-bold uppercase px-2 py-0.5 bg-orange-500/10 rounded">
                        Priority: {req.priority}
                      </span>
                    </div>

                    <p className="text-xs text-slate-400 leading-relaxed max-w-2xl">{req.motivation}</p>

                    <div className="flex flex-wrap items-center gap-4 text-[10px] text-slate-500 font-semibold pt-1">
                      <span className="flex items-center gap-1 text-slate-400">
                        <UserIcon className="h-3.5 w-3.5" />
                        {req.student?.full_name} ({req.student?.email})
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="h-3.5 w-3.5" />
                        Submitted {new Date(req.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>

                  <div className="flex sm:flex-row md:flex-col items-center gap-2 self-end md:self-start">
                    <button
                      onClick={() => handleApprove(req.id)}
                      disabled={approveMutation.isPending}
                      className="inline-flex items-center gap-1.5 px-3 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl text-xs transition-colors disabled:opacity-50"
                    >
                      <Check className="h-3.5 w-3.5 text-slate-950" />
                      <span>Approve</span>
                    </button>

                    <button
                      onClick={() => handleOpenRejectModal(req.id)}
                      className="inline-flex items-center gap-1.5 px-3 py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 font-bold rounded-xl text-xs transition-colors"
                    >
                      <X className="h-3.5 w-3.5" />
                      <span>Reject</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Section 2: Alumni Identity Verifications */}
      {activeTab === 'alumni' && (
        <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-slate-200">Alumni Identity & Credentials Verification</h2>
              <p className="text-slate-500 text-xs mt-0.5">Verify that alumni currently work at claimed enterprises before granting referral permissions</p>
            </div>

            <div className="relative w-full sm:w-72">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
              <input
                type="text"
                placeholder="Search alumni..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2 pl-9 pr-3 text-xs text-slate-200 focus:outline-none placeholder-slate-500"
              />
            </div>
          </div>

          {isLoadingAlumni ? (
            <div className="flex justify-center items-center py-16">
              <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-sky-400" />
            </div>
          ) : filteredAlumni.length === 0 ? (
            <div className="p-12 text-center">
              <HelpCircle className="h-10 w-10 text-slate-600 mx-auto mb-3" />
              <h4 className="font-bold text-slate-400 text-sm">No Alumni Registered Yet</h4>
              <p className="text-slate-600 text-xs mt-0.5">Newly registered alumni will appear here for verification.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredAlumni.map((item) => (
                <div 
                  key={item.id}
                  className="border border-slate-850 hover:border-slate-800 bg-slate-900/10 p-5 rounded-2xl transition-all flex flex-col md:flex-row md:items-start justify-between gap-4"
                >
                  <div className="space-y-2 flex-1">
                    <div className="flex items-center gap-3">
                      <h4 className="font-extrabold text-sm text-slate-200">{item.user_name}</h4>
                      {item.is_verified ? (
                        <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full">
                          <BadgeCheck className="h-3 w-3" />
                          <span>Verified</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[10px] font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-full">
                          <Clock className="h-3 w-3" />
                          <span>Pending Verification</span>
                        </span>
                      )}
                    </div>

                    <div className="text-xs text-slate-400 space-y-1">
                      <p><span className="text-slate-500 font-semibold">Email:</span> {item.user_email}</p>
                      <p>
                        <span className="text-slate-500 font-semibold">Role:</span> {item.current_position || 'Engineer'} at {item.current_company_name || 'Enterprise'}
                      </p>
                      <p>
                        <span className="text-slate-500 font-semibold">Graduation:</span> {item.graduation_year || 'N/A'} ({item.degree || 'Degree'} - {item.department || 'Dept'})
                      </p>
                    </div>

                    {item.linkedin_url && (
                      <a 
                        href={item.linkedin_url} 
                        target="_blank" 
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-xs text-sky-400 hover:text-sky-300 font-bold pt-1"
                      >
                        <span>View LinkedIn Profile</span>
                        <ExternalLink className="h-3 w-3" />
                      </a>
                    )}
                  </div>

                  <div className="flex sm:flex-row md:flex-col items-center gap-2 self-end md:self-start">
                    {!item.is_verified ? (
                      <button
                        onClick={() => verifyAlumniMutation.mutate(item.user_id)}
                        disabled={verifyAlumniMutation.isPending}
                        className="inline-flex items-center gap-1.5 px-3 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl text-xs transition-colors disabled:opacity-50"
                      >
                        <Check className="h-3.5 w-3.5" />
                        <span>Verify Identity</span>
                      </button>
                    ) : (
                      <button
                        onClick={() => rejectAlumniMutation.mutate(item.user_id)}
                        disabled={rejectAlumniMutation.isPending}
                        className="inline-flex items-center gap-1.5 px-3 py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 font-bold rounded-xl text-xs transition-colors disabled:opacity-50"
                      >
                        <X className="h-3.5 w-3.5" />
                        <span>Revoke Status</span>
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Reject Modal Confirmation */}
      {isRejectModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-md p-4">
          <div className="bg-slate-950 border border-slate-800 rounded-3xl w-full max-w-md p-6 relative overflow-hidden shadow-2xl animate-fade-in text-slate-200">
            <div className="absolute top-0 right-0 -mt-12 -mr-12 h-36 w-36 rounded-full bg-rose-500/5 blur-2xl" />
            
            <h2 className="text-lg font-extrabold flex items-center gap-2 border-b border-slate-800/60 pb-3">
              <ShieldAlert className="h-5 w-5 text-rose-400" />
              <span>Confirm Rejection</span>
            </h2>

            <form onSubmit={handleRejectSubmit} className="space-y-4 mt-6">
              <div>
                <label className="label text-xs text-slate-400 uppercase">Reason for Rejection *</label>
                <textarea
                  rows={4}
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                  placeholder="Provide clear feedback explaining why this request cannot be approved (e.g. Motivation lacks detail, Resume link is private, Skills mismatch)..."
                  className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2.5 px-4 text-xs text-slate-300 focus:outline-none"
                />
              </div>

              <div className="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-slate-800/60">
                <button
                  type="button"
                  onClick={() => setIsRejectModalOpen(false)}
                  className="px-4 py-2 text-xs font-bold text-slate-400 hover:text-slate-200 hover:bg-slate-900 rounded-lg transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={rejectMutation.isPending || !rejectReason.trim()}
                  className="inline-flex items-center gap-1.5 px-5 py-2.5 bg-rose-500 hover:bg-rose-400 text-slate-950 font-bold rounded-xl transition-all shadow-lg text-xs"
                >
                  <MessageSquare className="h-3.5 w-3.5 text-slate-950" />
                  <span>{rejectMutation.isPending ? 'Rejecting...' : 'Reject Request'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;
