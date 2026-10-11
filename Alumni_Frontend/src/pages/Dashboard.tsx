import { useAuthStore } from '../store/auth';
import { useQuery } from '@tanstack/react-query';
import { userApi } from '../services/user.service';
import { 
  Briefcase, 
  CheckCircle, 
  Clock, 
  ArrowRight, 
  Building2, 
  Users,
  Activity
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
    full_name: 'Member',
    email: '',
    role: 'student' as const,
  };

  const { data: dashboardResponse, isLoading } = useQuery({
    queryKey: ['dashboard-real-stats'],
    queryFn: () => userApi.getDashboardStats(),
    enabled: !!user,
  });

  const dashboardData = dashboardResponse?.data;
  const rawStats = dashboardData?.stats || [];
  const chartData = dashboardData?.chart_data || [];
  const statusPieData = dashboardData?.status_pie_data || [];
  const recentActivities = dashboardData?.recent_activities || [];

  const getStatIconAndColor = (type: string, idx: number) => {
    if (type === 'pending') {
      return { icon: Clock, color: 'from-amber-500 to-orange-600', shadow: 'shadow-amber-500/10' };
    }
    if (type === 'approved') {
      return { icon: CheckCircle, color: 'from-emerald-500 to-teal-600', shadow: 'shadow-emerald-500/10' };
    }
    if (type === 'total') {
      return { icon: Briefcase, color: 'from-sky-500 to-blue-600', shadow: 'shadow-sky-500/10' };
    }
    const icons = [Building2, Users, Activity];
    const colors = ['from-purple-500 to-indigo-600', 'from-pink-500 to-rose-600', 'from-cyan-500 to-blue-600'];
    return { icon: icons[idx % icons.length], color: colors[idx % colors.length], shadow: 'shadow-purple-500/10' };
  };

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
                {currentUser.full_name || 'Member'}
              </span>
              !
            </h1>
            <p className="text-slate-400 mt-2 max-w-xl text-sm leading-relaxed">
              AlumniConnect verified platform connecting students with high-achieving alumni for corporate job referrals. 
              {currentUser.role === 'student' && ' Submit targeted referral requests to verified company insiders.'}
              {currentUser.role === 'alumni' && ' Review pre-vetted student candidates and submit employee referrals.'}
              {currentUser.role === 'admin' && ' Review and manage student requests and verify alumni credentials.'}
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

      {/* Real Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {isLoading ? (
          [1, 2, 3].map((n) => (
            <div key={n} className="h-28 rounded-2xl bg-slate-950 border border-slate-850 animate-pulse" />
          ))
        ) : (
          rawStats.map((stat, idx) => {
            const { icon: Icon, color, shadow } = getStatIconAndColor(stat.type, idx);
            return (
              <div 
                key={idx}
                className={`relative overflow-hidden rounded-2xl bg-slate-950 border border-slate-800/80 p-6 flex items-center justify-between shadow-lg transition-transform hover:scale-[1.01] hover:border-slate-700/60 ${shadow}`}
              >
                <div className="space-y-2">
                  <span className="text-xs uppercase tracking-wider text-slate-500 font-semibold">{stat.label}</span>
                  <h3 className="text-4xl font-black text-slate-100">{stat.value}</h3>
                </div>
                <div className={`p-4 rounded-2xl bg-gradient-to-tr ${color} text-slate-950 shadow-md shadow-slate-950/20`}>
                  <Icon className="h-6 w-6 text-slate-950" />
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Charts section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Chart */}
        <div className="lg:col-span-2 bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-bold text-lg text-slate-200">System Activity</h3>
              <p className="text-slate-500 text-xs mt-0.5">Real-time referral milestone statistics</p>
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

        {/* Status Breakdown Pie Chart */}
        <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl flex flex-col">
          <h3 className="font-bold text-lg text-slate-200">Referral Status Breakdown</h3>
          <p className="text-slate-500 text-xs mt-0.5 mb-6">Distribution across live requests</p>
          
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
              <span className="block text-2xl font-black">Live</span>
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

      {/* Bottom Layout - Recent Real Activity & Info */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Real Activity */}
        <div className="lg:col-span-2 bg-slate-950 border border-slate-800/80 rounded-3xl p-6 shadow-xl">
          <h3 className="font-bold text-lg text-slate-200 mb-6">Recent Live Activity</h3>
          {recentActivities.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs">
              No recent requests yet. Submit a referral request to start the process!
            </div>
          ) : (
            <div className="space-y-6">
              {recentActivities.map((act) => (
                <div key={act.id} className="flex gap-4 group">
                  <div className="relative">
                    <div className={`h-10 w-10 rounded-full flex items-center justify-center text-xs font-bold shadow-md ${
                      act.status === 'approved' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 
                      act.status === 'pending' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 
                      act.status === 'fulfilled' ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20' :
                      'bg-slate-500/10 text-slate-400 border border-slate-500/20'
                    }`}>
                      {act.status === 'approved' ? <CheckCircle className="h-4 w-4" /> : 
                       act.status === 'pending' ? <Clock className="h-4 w-4" /> : 
                       <Briefcase className="h-4 w-4" />}
                    </div>
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
          )}
        </div>

        {/* Informative Side Card */}
        <div className="bg-gradient-to-b from-slate-950 to-slate-900 border border-slate-800/80 rounded-3xl p-6 shadow-xl flex flex-col justify-between">
          <div className="space-y-4">
            <h3 className="font-bold text-lg text-slate-200">How The Process Works</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              1. **Student submits** a referral request with target position, motivation, and skills alignment.
            </p>
            <p className="text-xs text-slate-400 leading-relaxed">
              2. **University Admin reviews** and verifies the request quality before approving.
            </p>
            <p className="text-xs text-slate-400 leading-relaxed">
              3. **Verified Alumni browse** approved requests and file internal corporate referrals.
            </p>
          </div>
          <div className="border-t border-slate-800/60 pt-4 mt-6">
            <span className="block text-[10px] uppercase tracking-wider text-slate-500 font-bold mb-2">Need Help?</span>
            <p className="text-[11px] text-slate-400">Contact the campus placement coordinator or check official platform guides.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
