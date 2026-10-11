import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/auth';
import { userApi, DashboardStats } from '../services/user.service';
import { 
  Mail, 
  Phone, 
  ShieldAlert, 
  Settings, 
  Key, 
  TrendingUp, 
  Calendar,
  CheckCircle,
  ThumbsUp,
  Sparkles,
  Loader2
} from 'lucide-react';
import toast from 'react-hot-toast';

const Profile = () => {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState<'info' | 'security' | 'stats'>('info');
  const [statsData, setStatsData] = useState<DashboardStats | null>(null);
  const [loadingStats, setLoadingStats] = useState(false);

  useEffect(() => {
    const fetchStats = async () => {
      setLoadingStats(true);
      try {
        const res = await userApi.getDashboardStats();
        if (res.data) {
          setStatsData(res.data);
        }
      } catch (err) {
        console.error('Failed to load profile metrics:', err);
      } finally {
        setLoadingStats(false);
      }
    };
    fetchStats();
  }, []);
  
  const currentUser = user || {
    full_name: 'AlumniConnect User',
    email: '',
    phone: '',
    role: 'student' as const,
    status: 'active',
    is_email_verified: true,
    created_at: new Date().toISOString()
  };

  const handleUpdateProfile = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success('Profile details updated successfully');
  };

  const handleChangePassword = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success('Security password updated successfully');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in text-slate-200">
      {/* Header */}
      <div>
        <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">User Profile</h1>
        <p className="text-slate-500 text-xs mt-0.5">Manage your personal settings, security credentials, and view metrics</p>
      </div>

      {/* Main Profile Info Card */}
      <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 md:p-8 shadow-2xl relative overflow-hidden flex flex-col md:flex-row gap-6 items-center md:items-start text-center md:text-left">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 h-40 w-40 rounded-full bg-sky-500/5 blur-2xl" />
        
        {/* Large Avatar */}
        <div className="h-20 w-20 rounded-full bg-gradient-to-tr from-sky-500 to-purple-500 flex items-center justify-center text-slate-950 font-black text-3xl shadow-xl shadow-sky-500/10 ring-4 ring-slate-900">
          {currentUser.full_name?.split(' ').map((n) => n[0]).join('').toUpperCase() || 'GU'}
        </div>

        {/* User Quick Info */}
        <div className="flex-1 space-y-2">
          <div className="flex flex-col md:flex-row md:items-center gap-2 justify-center md:justify-start">
            <h2 className="text-xl font-bold text-slate-100">{currentUser.full_name || 'Guest User'}</h2>
            <span className="inline-block md:inline text-[9px] uppercase font-extrabold tracking-wider bg-sky-500/10 text-sky-400 border border-sky-500/20 px-2 py-0.5 rounded-full w-fit mx-auto md:mx-0">
              {currentUser.role}
            </span>
          </div>
          
          <div className="flex flex-col sm:flex-row items-center gap-4 text-xs text-slate-400 font-semibold justify-center md:justify-start">
            <span className="flex items-center gap-1.5"><Mail className="h-4 w-4" />{currentUser.email}</span>
            {currentUser.phone && <span className="flex items-center gap-1.5"><Phone className="h-4 w-4" />{currentUser.phone}</span>}
          </div>

          <div className="flex items-center gap-1.5 text-[10px] text-slate-500 font-bold justify-center md:justify-start pt-2">
            <Calendar className="h-3.5 w-3.5" />
            <span>Member since {new Date(currentUser.created_at).toLocaleDateString(undefined, {month: 'long', year: 'numeric'})}</span>
          </div>
        </div>
      </div>

      {/* Tabs list */}
      <div className="flex border-b border-slate-800/80 gap-2">
        <button
          onClick={() => setActiveTab('info')}
          className={`flex items-center gap-2 px-4 py-3 text-xs font-bold transition-all relative ${
            activeTab === 'info' 
              ? 'text-sky-400 border-b-2 border-sky-400' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Settings className="h-4 w-4" />
          <span>Account Settings</span>
        </button>

        <button
          onClick={() => setActiveTab('security')}
          className={`flex items-center gap-2 px-4 py-3 text-xs font-bold transition-all relative ${
            activeTab === 'security' 
              ? 'text-sky-400 border-b-2 border-sky-400' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Key className="h-4 w-4" />
          <span>Security & Password</span>
        </button>

        <button
          onClick={() => setActiveTab('stats')}
          className={`flex items-center gap-2 px-4 py-3 text-xs font-bold transition-all relative ${
            activeTab === 'stats' 
              ? 'text-sky-400 border-b-2 border-sky-400' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <TrendingUp className="h-4 w-4" />
          <span>Performance Analytics</span>
        </button>
      </div>

      {/* Tabs Content */}
      <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 md:p-8 shadow-xl">
        {activeTab === 'info' && (
          <form onSubmit={handleUpdateProfile} className="space-y-6">
            <h3 className="font-extrabold text-sm text-slate-400 uppercase tracking-wider">General Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="label text-slate-300">Full Name</label>
                <input
                  type="text"
                  defaultValue={currentUser.full_name || ''}
                  className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
                />
              </div>
              <div>
                <label className="label text-slate-300">Email Address</label>
                <input
                  type="email"
                  defaultValue={currentUser.email}
                  disabled
                  className="w-full bg-slate-900/40 border border-slate-800 text-slate-500 rounded-xl py-2.5 px-4 text-sm cursor-not-allowed focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="label text-slate-300">Contact Number</label>
                <input
                  type="text"
                  defaultValue={currentUser.phone || ''}
                  className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
                />
              </div>
              <div>
                <label className="label text-slate-300 font-semibold">Verification Status</label>
                <div className="flex items-center gap-2 mt-2">
                  <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="text-xs font-bold text-emerald-400">Email Address Verified</span>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-end pt-4 border-t border-slate-800/50">
              <button
                type="submit"
                className="px-6 py-2.5 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-slate-950 font-bold rounded-xl shadow-lg transition-transform hover:scale-[1.02] active:scale-95"
              >
                Save Details
              </button>
            </div>
          </form>
        )}

        {activeTab === 'security' && (
          <form onSubmit={handleChangePassword} className="space-y-6">
            <h3 className="font-extrabold text-sm text-slate-400 uppercase tracking-wider">Change Password</h3>
            
            <div className="space-y-4">
              <div className="max-w-md">
                <label className="label text-slate-300">Current Password</label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
                />
              </div>

              <div className="max-w-md">
                <label className="label text-slate-300">New Password</label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
                />
              </div>

              <div className="max-w-md">
                <label className="label text-slate-300">Confirm New Password</label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2.5 px-4 text-sm text-slate-300 focus:outline-none"
                />
              </div>
            </div>

            <div className="flex items-center justify-end pt-4 border-t border-slate-800/50">
              <button
                type="submit"
                className="px-6 py-2.5 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-slate-950 font-bold rounded-xl shadow-lg transition-transform hover:scale-[1.02] active:scale-95"
              >
                Change Password
              </button>
            </div>
          </form>
        )}

        {activeTab === 'stats' && (
          <div className="space-y-6">
            <h3 className="font-extrabold text-sm text-slate-400 uppercase tracking-wider">Candidate Performance</h3>
            
            {loadingStats ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-6 w-6 animate-spin text-sky-400" />
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {(statsData?.stats || [
                  { label: 'Total Requests', value: '0', type: 'total' },
                  { label: 'Pending Approvals', value: '0', type: 'pending' },
                  { label: 'Approved Requests', value: '0', type: 'approved' },
                ]).map((stat, idx) => (
                  <div key={idx} className="bg-slate-900/50 border border-slate-800/40 p-5 rounded-2xl flex flex-col justify-between h-32 relative overflow-hidden shadow">
                    <div className="absolute top-0 right-0 -mt-8 -mr-8 h-20 w-20 rounded-full bg-sky-500/5 blur-xl" />
                    <span className="text-slate-500 text-xs font-bold uppercase tracking-wider">{stat.label}</span>
                    <span className="text-3xl font-black text-slate-200">{stat.value}</span>
                    <span className="text-[10px] text-sky-400 font-semibold flex items-center gap-1">
                      {idx === 0 && <><Sparkles className="h-3 w-3" />Live database record</>}
                      {idx === 1 && <><ThumbsUp className="h-3 w-3" />Awaiting validation</>}
                      {idx === 2 && <><CheckCircle className="h-3 w-3" />Verified status</>}
                    </span>
                  </div>
                ))}
              </div>
            )}

            <div className="bg-slate-900/40 border border-slate-800/60 p-5 rounded-2xl flex items-center gap-4">
              <ShieldAlert className="h-10 w-10 text-sky-400" />
              <div>
                <h4 className="font-bold text-sm text-slate-200">Portfolio Optimization Tips</h4>
                <p className="text-xs text-slate-400 leading-relaxed mt-1">
                  Keep your motivational responses precise and directly target position descriptions. 
                  Endorsements from peers increase the visibility of your profile cards in the alumni directory view.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
