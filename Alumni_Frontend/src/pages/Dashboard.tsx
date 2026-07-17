import { useAuthStore } from '../store/auth';
import { useQuery } from '@tanstack/react-query';
import { referralRequestApi } from '../services/referral-request.service';
import { companyApi } from '../services/company.service';
import { 
  Briefcase, 
  CheckCircle, 
  Clock, 
  ArrowRight,
  TrendingUp,
  Building2,
  Users
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  PieChart, 
  Pie, 
  Cell 
} from 'recharts';

const Dashboard = () => {
  const { user } = useAuthStore();
  const currentUser = user || {
    full_name: 'Guest User',
    email: 'guest@example.com',
    role: 'student' as const,
  };

  // Queries (with mock fallback if backend endpoints are not seeded yet)
  const { data: requestsData } = useQuery({
    queryKey: ['my-requests'],
    queryFn: () => referralRequestApi.getAll(),
    enabled: !!user,
  });

  const { data: companiesData } = useQuery({
    queryKey: ['companies-list'],
    queryFn: () => companyApi.getAll(),
    enabled: !!user,
  });

  const requests = requestsData?.data || [];
  const companies = companiesData?.data || [];

  // Mock dashboard stats and chart data based on role
  const getStatsByRole = () => {
    if (currentUser.role === 'student') {
      const pendingCount = requests.filter(r => r.status === 'pending').length || 2;
      const approvedCount = requests.filter(r => r.status === 'approved').length || 1;
      const totalCount = requests.length || 3;
      return [
        { label: 'Total Requests', value: totalCount, icon: Briefcase, color: 'from-sky-500 to-blue-600', shadow: 'shadow-sky-500/10' },
        { label: 'Pending Approvals', value: pendingCount, icon: Clock, color: 'from-amber-500 to-orange-600', shadow: 'shadow-amber-500/10' },
        { label: 'Approved Requests', value: approvedCount, icon: CheckCircle, color: 'from-emerald-500 to-teal-600', shadow: 'shadow-emerald-500/10' },
      ];
    } else if (currentUser.role === 'alumni') {
      return [
        { label: 'Pending Referrals', value: 4, icon: Clock, color: 'from-amber-500 to-orange-600', shadow: 'shadow-amber-500/10' },
        { label: 'My Submissions', value: 8, icon: Briefcase, color: 'from-sky-500 to-blue-600', shadow: 'shadow-sky-500/10' },
        { label: 'Success Rate', value: '75%', icon: TrendingUp, color: 'from-emerald-500 to-teal-600', shadow: 'shadow-emerald-500/10' },
      ];
    } else { // admin
      return [
        { label: 'Pending Approvals', value: 12, icon: Clock, color: 'from-amber-500 to-orange-600', shadow: 'shadow-amber-500/10' },
        { label: 'Total Companies', value: companies.length || 45, icon: Building2, color: 'from-sky-500 to-blue-600', shadow: 'shadow-sky-500/10' },
        { label: 'Active Users', value: 128, icon: Users, color: 'from-purple-500 to-indigo-600', shadow: 'shadow-purple-500/10' },
      ];
    }
  };

  const chartData = [
    { name: 'Jan', referrals: 4, applications: 12 },
    { name: 'Feb', referrals: 7, applications: 15 },
    { name: 'Mar', referrals: 12, applications: 22 },
    { name: 'Apr', referrals: 18, applications: 30 },
    { name: 'May', referrals: 24, applications: 38 },
  ];

  const statusPieData = [
    { name: 'Pending', value: 40, color: '#f59e0b' },
    { name: 'Approved', value: 35, color: '#10b981' },
    { name: 'Rejected', value: 10, color: '#ef4444' },
    { name: 'Fulfilled', value: 15, color: '#0ea5e9' },
  ];

  // Recent Activity Feed
  const recentActivities = [
    { id: 1, title: 'Referral Request Approved', desc: 'Google L3 Frontend Engineer by Admin', time: '2 hours ago', status: 'approved' },
    { id: 2, title: 'New Request Created', desc: 'Microsoft Software Developer request', time: '5 hours ago', status: 'pending' },
    { id: 3, title: 'Skills Endorsed', desc: 'Suresh Kumar endorsed your React skills', time: '1 day ago', status: 'endorsed' },
  ];

  return (
    <div className="space-y-8 animate-fade-in text-slate-200">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 border border-slate-800/80 p-8 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 h-64 w-64 rounded-full bg-sky-500/5 blur-3xl" />
        <div className="absolute bottom-0 left-0 -mb-12 -ml-12 h-64 w-64 rounded-full bg-purple-500/5 blur-3xl" />
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">
              Welcome back,{' '}
              <span className="bg-gradient-to-r from-sky-400 to-purple-400 bg-clip-text text-transparent">
                {currentUser.full_name || 'Guest User'}
              </span>
              !
            </h1>
            <p className="text-slate-400 mt-2 max-w-xl text-sm leading-relaxed">
              Connecting students with high-achieving alumni for career growth and fast job referrals. 
              {currentUser.role === 'student' && ' Create referral requests to target premium companies!'}
              {currentUser.role === 'alumni' && ' Help students realize their potential by providing endorsements and referrals!'}
              {currentUser.role === 'admin' && ' Review and manage students and alumni submissions to maintain standard verification.'}
            </p>
          </div>
          {currentUser.role === 'student' && (
            <Link
              to="/requests/new"
              className="inline-flex items-center gap-2 px-6 py-3.5 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-slate-950 font-bold rounded-2xl shadow-xl shadow-sky-500/10 hover:shadow-sky-500/20 hover:scale-[1.02] active:scale-95 transition-all"
            >
              <span>Request Referral</span>
              <ArrowRight className="h-4 w-4 text-slate-950" />
            </Link>
          )}
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {getStatsByRole().map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <div 
              key={idx}
              className={`relative overflow-hidden rounded-2xl bg-slate-950 border border-slate-800/80 p-6 flex items-center justify-between shadow-lg transition-transform hover:scale-[1.01] hover:border-slate-700/60 ${stat.shadow}`}
            >
              <div className="space-y-2">
                <span className="text-xs uppercase tracking-wider text-slate-500 font-semibold">{stat.label}</span>
                <h3 className="text-4xl font-black text-slate-100">{stat.value}</h3>
              </div>
              <div className={`p-4 rounded-2xl bg-gradient-to-tr ${stat.color} text-slate-950 shadow-md shadow-slate-950/20`}>
                <Icon className="h-6 w-6 text-slate-950" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Chart */}
        <div className="lg:col-span-2 bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-bold text-lg text-slate-200">System Activity</h3>
              <p className="text-slate-500 text-xs mt-0.5">Monthly summary of job referrals and request creations</p>
            </div>
            <div className="flex items-center gap-4 text-xs font-semibold">
              <span className="flex items-center gap-1.5 text-sky-400">
                <span className="h-2 w-2 rounded-full bg-sky-500" /> Referrals
              </span>
              <span className="flex items-center gap-1.5 text-purple-400">
                <span className="h-2 w-2 rounded-full bg-purple-500" /> Applications
              </span>
            </div>
          </div>
          
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorReferrals" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorApps" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#a855f7" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#a855f7" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.3} />
                <XAxis dataKey="name" stroke="#64748b" fontSize={10} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#020617', border: '1px solid #1e293b', borderRadius: '12px' }}
                  labelStyle={{ color: '#94a3b8', fontSize: '12px', fontWeight: 'bold' }}
                />
                <Area type="monotone" dataKey="referrals" stroke="#0ea5e9" strokeWidth={2} fillOpacity={1} fill="url(#colorReferrals)" />
                <Area type="monotone" dataKey="applications" stroke="#a855f7" strokeWidth={2} fillOpacity={1} fill="url(#colorApps)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pie Chart */}
        <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl flex flex-col">
          <h3 className="font-bold text-lg text-slate-200">Referral Request Status</h3>
          <p className="text-slate-500 text-xs mt-0.5 mb-6">Distribution of overall request milestones</p>
          
          <div className="flex-1 flex items-center justify-center h-48 relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={statusPieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {statusPieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#020617', border: '1px solid #1e293b', borderRadius: '12px' }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute text-center">
              <span className="block text-2xl font-black">100%</span>
              <span className="text-[10px] uppercase text-slate-500 tracking-wider font-semibold">Tracked</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs font-semibold mt-4">
            {statusPieData.map((item, idx) => (
              <div key={idx} className="flex items-center gap-1.5 text-slate-400">
                <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                <span>{item.name} ({item.value}%)</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Layout - Recent Activity & Info */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Activity */}
        <div className="lg:col-span-2 bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl">
          <h3 className="font-bold text-lg text-slate-200 mb-6">Recent Activity Feed</h3>
          <div className="space-y-6">
            {recentActivities.map((act) => (
              <div key={act.id} className="flex gap-4 group">
                <div className="relative">
                  <div className={`h-10 w-10 rounded-full flex items-center justify-center text-xs font-bold shadow-md ${
                    act.status === 'approved' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 
                    act.status === 'pending' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 
                    'bg-sky-500/10 text-sky-400 border border-sky-500/20'
                  }`}>
                    {act.status === 'approved' ? <CheckCircle className="h-4 w-4" /> : 
                     act.status === 'pending' ? <Clock className="h-4 w-4" /> : 
                     <Users className="h-4 w-4" />}
                  </div>
                  {act.id !== recentActivities.length && (
                    <div className="absolute top-10 bottom-0 left-5 w-0.5 bg-slate-800 -mb-6" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-4">
                    <h4 className="text-sm font-bold text-slate-200 group-hover:text-sky-400 transition-colors">
                      {act.title}
                    </h4>
                    <span className="text-[10px] text-slate-500 whitespace-nowrap">{act.time}</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1 leading-normal">{act.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Informative Side Card */}
        <div className="bg-gradient-to-b from-slate-950 to-slate-900 border border-slate-800/80 rounded-3xl p-6 shadow-xl flex flex-col justify-between">
          <div className="space-y-4">
            <h3 className="font-bold text-lg text-slate-200">How Referrals Work</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              1. **Student submits** a referral request indicating their target role, motivation, resume, and experience.
            </p>
            <p className="text-xs text-slate-400 leading-relaxed">
              2. **Peer students endorse** the request to vouch for technical capability and character.
            </p>
            <p className="text-xs text-slate-400 leading-relaxed">
              3. **Alumni browse and refer** approved requests by writing internal referrals in their company portal.
            </p>
          </div>
          <div className="border-t border-slate-800/60 pt-4 mt-6">
            <span className="block text-[10px] uppercase tracking-wider text-slate-500 font-bold mb-2">Need Assistance?</span>
            <p className="text-[11px] text-slate-400">Reach out to the system administrator or check our documentation in the root path.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
