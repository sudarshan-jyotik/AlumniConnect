import { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import { 
  LayoutDashboard, 
  Briefcase, 
  Building2, 
  User, 
  Shield, 
  LogOut, 
  Bell, 
  Menu, 
  X,
  ChevronDown,
  GraduationCap
} from 'lucide-react';

const MainLayout = () => {
  const { user, clearAuth } = useAuthStore();
  const location = useLocation();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);

  // Current authenticated user
  const currentUser = user || {
    full_name: 'User',
    email: '',
    role: 'student' as const,
  };

  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  const navItems = [
    {
      label: 'Dashboard',
      path: '/dashboard',
      icon: LayoutDashboard,
      roles: ['student', 'alumni', 'admin'],
    },
    {
      label: 'Referral Requests',
      path: '/requests',
      icon: Briefcase,
      roles: ['student', 'alumni', 'admin'],
    },
    {
      label: 'Request Referral',
      path: '/requests/new',
      icon: GraduationCap,
      roles: ['student'], // Only students request referrals
    },
    {
      label: 'Companies',
      path: '/companies',
      icon: Building2,
      roles: ['student', 'alumni', 'admin'],
    },
    {
      label: 'Admin Panel',
      path: '/admin',
      icon: Shield,
      roles: ['admin'], // Only admins see admin panel
    },
    {
      label: 'Profile',
      path: '/profile',
      icon: User,
      roles: ['student', 'alumni', 'admin'],
    },
  ];

  const filteredNavItems = navItems.filter((item) => item.roles.includes(currentUser.role));

  const getPageTitle = () => {
    const current = navItems.find((item) => location.pathname.startsWith(item.path));
    return current ? current.label : 'AlumniConnect';
  };

  const [notifications, setNotifications] = useState<Array<{ id: number; text: string; time: string; read: boolean }>>([]);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex font-sans">
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-64 bg-slate-950/80 backdrop-blur-xl border-r border-slate-800/60 p-4 transition-all duration-300">
        <div className="flex items-center gap-3 px-3 py-4 mb-8 border-b border-slate-800/60">
          <div className="bg-gradient-to-tr from-sky-400 to-purple-500 p-2 rounded-xl text-slate-950 shadow-lg shadow-sky-500/20">
            <GraduationCap className="h-6 w-6" />
          </div>
          <div>
            <span className="font-bold text-lg bg-gradient-to-r from-sky-400 to-purple-400 bg-clip-text text-transparent">
              AlumniConnect
            </span>
            <span className="block text-[10px] uppercase tracking-wider text-slate-500 font-semibold">
              Referral Hub
            </span>
          </div>
        </div>

        <nav className="flex-1 space-y-1.5">
          {filteredNavItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path || (item.path !== '/dashboard' && location.pathname.startsWith(item.path));
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all duration-200 group ${
                  isActive
                    ? 'bg-gradient-to-r from-sky-500/20 to-purple-500/10 text-sky-400 border-l-4 border-sky-400'
                    : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
                }`}
              >
                <Icon className={`h-5 w-5 transition-transform duration-200 ${isActive ? 'scale-110' : 'group-hover:scale-110'}`} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* User Card */}
        <div className="mt-auto border-t border-slate-800/60 pt-4">
          <div className="flex items-center gap-3 px-3 py-2 bg-slate-900/40 rounded-xl border border-slate-800/40">
            <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-sky-500 to-purple-500 flex items-center justify-center text-slate-950 font-bold text-sm shadow-md">
              {currentUser.full_name?.split(' ').map((n) => n[0]).join('').toUpperCase() || 'GU'}
            </div>
            <div className="flex-1 min-w-0">
              <span className="block font-semibold text-sm truncate">{currentUser.full_name || 'Guest User'}</span>
              <span className="block text-[10px] text-slate-500 uppercase tracking-wider font-semibold">
                {currentUser.role}
              </span>
            </div>
            <button 
              onClick={handleLogout}
              className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-800/50 rounded-lg transition-colors"
              title="Sign Out"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Mobile Menu Backdrop */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 z-40 bg-slate-950/60 backdrop-blur-sm md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Mobile Sidebar */}
      <aside 
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-slate-950 border-r border-slate-800 flex flex-col p-4 transform transition-transform duration-300 md:hidden ${
          isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between px-3 py-4 mb-8 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <div className="bg-gradient-to-tr from-sky-400 to-purple-500 p-2 rounded-xl text-slate-950">
              <GraduationCap className="h-5 w-5" />
            </div>
            <span className="font-bold text-lg text-slate-200">AlumniConnect</span>
          </div>
          <button 
            onClick={() => setIsMobileMenuOpen(false)}
            className="p-1 rounded-lg text-slate-400 hover:bg-slate-800"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="flex-1 space-y-1.5">
          {filteredNavItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path || (item.path !== '/dashboard' && location.pathname.startsWith(item.path));
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all group ${
                  isActive
                    ? 'bg-gradient-to-r from-sky-500/20 to-purple-500/10 text-sky-400 border-l-4 border-sky-400'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`}
              >
                <Icon className="h-5 w-5" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto border-t border-slate-800 pt-4">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-4 py-3 rounded-xl font-medium text-slate-400 hover:bg-slate-800 hover:text-red-400 transition-colors"
          >
            <LogOut className="h-5 w-5" />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen">
        {/* Header */}
        <header className="h-16 bg-slate-900/60 backdrop-blur-xl border-b border-slate-800/60 flex items-center justify-between px-6 sticky top-0 z-30">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setIsMobileMenuOpen(true)}
              className="p-2 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-slate-200 md:hidden"
            >
              <Menu className="h-5 w-5" />
            </button>
            <h2 className="text-xl font-bold text-slate-200 hidden md:block">
              {getPageTitle()}
            </h2>
          </div>

          <div className="flex items-center gap-4">
            {/* Notifications Hub */}
            <div className="relative">
              <button 
                onClick={() => {
                  setIsNotificationsOpen(!isNotificationsOpen);
                  setIsProfileDropdownOpen(false);
                }}
                className={`p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 transition-colors relative ${
                  isNotificationsOpen ? 'bg-slate-800 text-slate-200' : ''
                }`}
              >
                <Bell className="h-5 w-5" />
                {notifications.some(n => !n.read) && (
                  <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-sky-500 ring-2 ring-slate-900" />
                )}
              </button>

              {isNotificationsOpen && (
                <div className="absolute right-0 mt-2 w-80 bg-slate-950 border border-slate-800/80 rounded-2xl shadow-2xl p-2 z-50 animate-slide-in">
                  <div className="px-3 py-2 border-b border-slate-800/60 flex items-center justify-between">
                    <span className="font-bold text-sm">Notifications</span>
                    {notifications.length > 0 && (
                      <button 
                        onClick={() => setNotifications(notifications.map(n => ({ ...n, read: true })))}
                        className="text-[10px] text-sky-400 hover:underline"
                      >
                        Mark all as read
                      </button>
                    )}
                  </div>
                  <div className="divide-y divide-slate-800/40 max-h-64 overflow-y-auto">
                    {notifications.length === 0 ? (
                      <div className="p-6 text-center text-xs text-slate-500">
                        No new notifications
                      </div>
                    ) : (
                      notifications.map((n) => (
                        <div key={n.id} className="p-3 hover:bg-slate-900/40 rounded-xl transition-colors cursor-pointer group">
                          <p className={`text-xs ${n.read ? 'text-slate-400' : 'text-slate-200 font-semibold'}`}>
                            {n.text}
                          </p>
                          <span className="block text-[9px] text-slate-500 mt-1">{n.time}</span>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Profile Dropdown */}
            <div className="relative">
              <button 
                onClick={() => {
                  setIsProfileDropdownOpen(!isProfileDropdownOpen);
                  setIsNotificationsOpen(false);
                }}
                className="flex items-center gap-2 p-1.5 rounded-xl hover:bg-slate-800/50 transition-colors"
              >
                <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-sky-500 to-purple-500 flex items-center justify-center text-slate-950 font-bold text-xs shadow-md">
                  {currentUser.full_name?.split(' ').map((n) => n[0]).join('').toUpperCase() || 'GU'}
                </div>
                <ChevronDown className="h-4 w-4 text-slate-400 hidden sm:block" />
              </button>

              {isProfileDropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-slate-950 border border-slate-800/80 rounded-2xl shadow-2xl p-2 z-50 animate-slide-in">
                  <div className="px-3 py-2 border-b border-slate-800/60">
                    <span className="block font-semibold text-xs truncate">{currentUser.full_name || 'Guest User'}</span>
                    <span className="block text-[9px] text-slate-500 lowercase truncate">{currentUser.email}</span>
                  </div>
                  <div className="py-1">
                    <Link 
                      to="/profile" 
                      onClick={() => setIsProfileDropdownOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs text-slate-400 hover:text-slate-200 hover:bg-slate-900/50 rounded-lg transition-colors"
                    >
                      <User className="h-3.5 w-3.5" />
                      <span>My Profile</span>
                    </Link>
                    <button 
                      onClick={handleLogout}
                      className="flex items-center gap-2 w-full text-left px-3 py-2 text-xs text-red-400 hover:bg-red-500/10 rounded-lg transition-colors mt-1"
                    >
                      <LogOut className="h-3.5 w-3.5" />
                      <span>Sign Out</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Content Outlet */}
        <main className="flex-1 p-6 md:p-8 overflow-y-auto bg-slate-900/40">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
