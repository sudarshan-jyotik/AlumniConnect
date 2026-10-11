import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { referralRequestApi } from '../services/referral-request.service';
import { useAuthStore } from '../store/auth';
import { Link } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  MapPin, 
  Calendar, 
  ThumbsUp, 
  ChevronRight, 
  Plus,
  HelpCircle
} from 'lucide-react';

const ReferralRequests = () => {
  const { user } = useAuthStore();
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');

  const { data: response, isLoading } = useQuery({
    queryKey: ['referral-requests-list'],
    queryFn: () => referralRequestApi.getAll(),
  });

  const rawRequests = response?.data || [];

  const requests = rawRequests;

  // Filter requests
  const filteredRequests = requests.filter((req) => {
    const matchesSearch = 
      req.position_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (req.company?.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (req.student?.full_name || '').toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || req.status === statusFilter;
    const matchesPriority = priorityFilter === 'all' || req.priority === priorityFilter;

    return matchesSearch && matchesStatus && matchesPriority;
  });

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

  const getPriorityStyle = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return 'bg-red-500/20 text-red-300';
      case 'high':
        return 'bg-orange-500/20 text-orange-300';
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-300';
      default:
        return 'bg-slate-800 text-slate-400';
    }
  };

  return (
    <div className="space-y-6 animate-fade-in text-slate-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">Referral Requests</h1>
          <p className="text-slate-500 text-xs mt-0.5">Browse through active student requests for company referrals</p>
        </div>
        {user?.role === 'student' && (
          <Link
            to="/requests/new"
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-slate-950 font-bold rounded-xl shadow-lg transition-transform hover:scale-[1.02] active:scale-95"
          >
            <Plus className="h-4 w-4 text-slate-950" />
            <span>Create Request</span>
          </Link>
        )}
      </div>

      {/* Filters Hub */}
      <div className="bg-slate-950 border border-slate-800/80 rounded-2xl p-4 shadow-xl flex flex-col md:flex-row gap-4">
        {/* Search */}
        <div className="flex-1 relative">
          <Search className="absolute left-3.5 top-3 h-4.5 w-4.5 text-slate-500" />
          <input
            type="text"
            placeholder="Search by position, company, or student..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 pl-11 pr-4 text-sm text-slate-200 focus:outline-none placeholder-slate-500"
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-slate-500" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs font-semibold focus:outline-none focus:border-sky-500 text-slate-300"
            >
              <option value="all">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="fulfilled">Fulfilled</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs font-semibold focus:outline-none focus:border-sky-500 text-slate-300"
            >
              <option value="all">All Priorities</option>
              <option value="urgent">Urgent</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </div>
      </div>

      {/* Catalog Cards Grid */}
      {isLoading ? (
        <div className="flex justify-center items-center py-24">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-400" />
        </div>
      ) : filteredRequests.length === 0 ? (
        <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-12 text-center shadow-xl">
          <HelpCircle className="h-12 w-12 text-slate-600 mx-auto mb-4" />
          <h3 className="font-bold text-slate-300 text-lg">No Referral Requests Found</h3>
          <p className="text-slate-500 text-xs mt-1">Try adjusting your filters or search keywords.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredRequests.map((req) => (
            <div 
              key={req.id} 
              className="bg-slate-950 border border-slate-800/80 rounded-2xl p-6 shadow-lg flex flex-col justify-between hover:border-slate-700/60 hover:shadow-2xl transition-all duration-300 group hover:scale-[1.01]"
            >
              <div>
                {/* Upper line: Company + Badges */}
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="text-lg font-bold text-slate-100 group-hover:text-sky-400 transition-colors">
                      {req.position_title}
                    </h3>
                    <span className="text-sky-400 font-semibold text-sm block mt-0.5">{req.company.name}</span>
                  </div>
                  <div className="flex flex-col items-end gap-1.5">
                    <span className={`text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded-full ${getStatusStyle(req.status)}`}>
                      {req.status}
                    </span>
                    <span className={`text-[9px] uppercase font-extrabold tracking-wider px-2 py-0.5 rounded ${getPriorityStyle(req.priority)}`}>
                      {req.priority}
                    </span>
                  </div>
                </div>

                {/* Motivation summary */}
                <p className="text-xs text-slate-400 mt-4 leading-relaxed line-clamp-3">
                  {req.motivation}
                </p>

                {/* Meta details */}
                <div className="grid grid-cols-2 gap-4 mt-6 pt-4 border-t border-slate-800/50 text-[11px] text-slate-500 font-semibold">
                  <div className="flex items-center gap-1.5">
                    <MapPin className="h-3.5 w-3.5" />
                    <span>{req.location || 'Not Specified'}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Calendar className="h-3.5 w-3.5" />
                    <span>{new Date(req.created_at).toLocaleDateString(undefined, {month: 'short', day: 'numeric', year: 'numeric'})}</span>
                  </div>
                </div>
              </div>

              {/* Bottom Actions */}
              <div className="flex items-center justify-between mt-6 pt-4 border-t border-slate-800/50">
                <div className="flex items-center gap-4">
                  <span className="flex items-center gap-1.5 text-xs text-slate-400 font-bold">
                    <ThumbsUp className="h-4 w-4 text-sky-500" />
                    <span>{req.endorsement_count || 0} Endorsement(s)</span>
                  </span>
                </div>
                <Link
                  to={`/requests/${req.id}`}
                  className="inline-flex items-center gap-1 text-xs font-bold text-sky-400 hover:text-sky-300 transition-colors group-hover:translate-x-1 duration-200"
                >
                  <span>View Details</span>
                  <ChevronRight className="h-4 w-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ReferralRequests;
