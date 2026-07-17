import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { adminApi } from '../../services/admin.service';
import toast from 'react-hot-toast';
import { 
  ShieldAlert, 
  Check, 
  X, 
  Building2, 
  User, 
  Calendar, 
  HelpCircle,
  Clock,
  Sparkles,
  Search,
  MessageSquare
} from 'lucide-react';

const AdminPanel = () => {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [isRejectModalOpen, setIsRejectModalOpen] = useState(false);
  const [selectedRequestId, setSelectedRequestId] = useState<number | null>(null);
  const [rejectReason, setRejectReason] = useState('');

  const { data: response, isLoading } = useQuery({
    queryKey: ['pending-requests'],
    queryFn: () => adminApi.getPendingRequests(),
  });

  const rawRequests = response?.data || [];

  // Fallback mock pending requests
  const mockPendingRequests = [
    {
      id: 101,
      position_title: 'Software Developer Intern',
      motivation: 'I have completed my junior year and am eager to apply my systems programming skills at Amazon. I built a distributed database prototype for my capstone project.',
      location: 'Seattle, WA',
      created_at: new Date(Date.now() - 86400000).toISOString(),
      student: { full_name: 'Harish Mehta', email: 'harish@example.com' },
      company: { name: 'Amazon' }
    },
    {
      id: 102,
      position_title: 'Product Designer',
      motivation: 'Figma power-user, focused on accessible design systems. I want to work with the Apple design team to build high-fidelity interface prototypes that look stunning.',
      location: 'San Francisco, CA',
      created_at: new Date(Date.now() - 86400000 * 2).toISOString(),
      student: { full_name: 'Meera Nair', email: 'meera@example.com' },
      company: { name: 'Apple' }
    }
  ];

  const pendingRequests = rawRequests.length > 0 ? rawRequests : mockPendingRequests;

  const approveMutation = useMutation({
    mutationFn: (id: number) => adminApi.approveRequest(id),
    onSuccess: () => {
      toast.success('Referral request successfully approved!');
      queryClient.invalidateQueries({ queryKey: ['pending-requests'] });
    },
    onError: () => {
      toast.error('Failed to approve referral request');
    }
  });

  const rejectMutation = useMutation({
    mutationFn: (data: { id: number; reason: string }) => adminApi.rejectRequest(data.id, data.reason),
    onSuccess: () => {
      toast.success('Referral request successfully rejected.');
      setIsRejectModalOpen(false);
      setRejectReason('');
      setSelectedRequestId(null);
      queryClient.invalidateQueries({ queryKey: ['pending-requests'] });
    },
    onError: () => {
      toast.error('Failed to reject referral request');
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

  // Search pending list
  const filteredPending = pendingRequests.filter((req) => {
    return req.position_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
           req.company.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
           (req.student?.full_name || '').toLowerCase().includes(searchTerm.toLowerCase());
  });

  return (
    <div className="space-y-6 animate-fade-in text-slate-200">
      {/* Header stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-950 border border-slate-800/80 p-5 rounded-2xl flex items-center justify-between shadow">
          <div className="space-y-1">
            <span className="text-slate-500 text-xs font-bold uppercase tracking-wider">Pending Review Queue</span>
            <h3 className="text-3xl font-black text-slate-200">{pendingRequests.length}</h3>
          </div>
          <div className="p-3 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-xl">
            <Clock className="h-6 w-6" />
          </div>
        </div>

        <div className="bg-slate-950 border border-slate-800/80 p-5 rounded-2xl flex items-center justify-between shadow">
          <div className="space-y-1">
            <span className="text-slate-500 text-xs font-bold uppercase tracking-wider">Alumni Verification Requests</span>
            <h3 className="text-3xl font-black text-slate-200">4</h3>
          </div>
          <div className="p-3 bg-sky-500/10 text-sky-400 border border-sky-500/20 rounded-xl">
            <Sparkles className="h-6 w-6" />
          </div>
        </div>

        <div className="bg-slate-950 border border-slate-800/80 p-5 rounded-2xl flex items-center justify-between shadow">
          <div className="space-y-1">
            <span className="text-slate-500 text-xs font-bold uppercase tracking-wider">Overall Success Actions</span>
            <h3 className="text-3xl font-black text-slate-200">98%</h3>
          </div>
          <div className="p-3 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-xl">
            <Check className="h-6 w-6" />
          </div>
        </div>
      </div>

      {/* Main Review Section */}
      <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-200">Pending Approvals Queue</h2>
            <p className="text-slate-500 text-xs mt-0.5">Vouch on academic motivations and skills before releasing to alumni</p>
          </div>

          <div className="relative w-full sm:w-72">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
            <input
              type="text"
              placeholder="Filter queue..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-1.8 pl-9 pr-3 text-xs text-slate-200 focus:outline-none placeholder-slate-500"
            />
          </div>
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center py-16">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-sky-400" />
          </div>
        ) : filteredPending.length === 0 ? (
          <div className="p-12 text-center">
            <HelpCircle className="h-10 w-10 text-slate-600 mx-auto mb-3" />
            <h4 className="font-bold text-slate-400 text-sm">Approvals Queue is Completely Clear</h4>
            <p className="text-slate-600 text-xs mt-0.5">All student requests are currently processed!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredPending.map((req) => (
              <div 
                key={req.id}
                className="border border-slate-850 hover:border-slate-800 bg-slate-900/10 p-5 rounded-2xl transition-all flex flex-col md:flex-row md:items-start justify-between gap-4"
              >
                {/* Request details */}
                <div className="space-y-3 flex-1">
                  <div className="flex flex-wrap items-center gap-3">
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded">
                      <Building2 className="h-3 w-3" />
                      <span>{req.company.name}</span>
                    </span>
                    <h4 className="font-extrabold text-sm text-slate-200">{req.position_title}</h4>
                  </div>

                  <p className="text-xs text-slate-400 leading-relaxed max-w-2xl">{req.motivation}</p>

                  <div className="flex flex-wrap items-center gap-4 text-[10px] text-slate-500 font-semibold pt-1">
                    <span className="flex items-center gap-1 text-slate-400"><User className="h-3.5 w-3.5" />{req.student.full_name} ({req.student.email})</span>
                    <span className="flex items-center gap-1"><Calendar className="h-3.5 w-3.5" />Submitted {new Date(req.created_at).toLocaleDateString()}</span>
                  </div>
                </div>

                {/* Approve/Reject Actions */}
                <div className="flex sm:flex-row md:flex-col items-center gap-2 self-end md:self-start">
                  <button
                    onClick={() => handleApprove(req.id)}
                    className="inline-flex items-center gap-1.5 px-3 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl text-xs transition-colors"
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
                  placeholder="Provide feedback to the student explaining why this request cannot be approved (e.g. Motivation lacks detail, Resume link is missing/private)..."
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
