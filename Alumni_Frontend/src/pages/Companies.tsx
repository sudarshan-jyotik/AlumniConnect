import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { companyApi } from '../services/company.service';
import { useAuthStore } from '../store/auth';
import toast from 'react-hot-toast';
import { 
  Building2, 
  Search, 
  Plus, 
  Globe, 
  MapPin, 
  Users, 
  Briefcase,
  HelpCircle,
  X,
  Send
} from 'lucide-react';

const Companies = () => {
  const { user } = useAuthStore();
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  
  // Create Company form state
  const [name, setName] = useState('');
  const [industry, setIndustry] = useState('');
  const [website, setWebsite] = useState('');
  const [careersPage, setCareersPage] = useState('');
  const [description, setDescription] = useState('');
  const [headquarters, setHeadquarters] = useState('');
  const [companySize, setCompanySize] = useState('100-500');

  const { data: response, isLoading } = useQuery({
    queryKey: ['companies-list-main'],
    queryFn: () => companyApi.getAll(),
  });

  const rawCompanies: any[] = response?.data || [];

  // Fallback companies list for presentation
  const mockCompanies = [
    {
      id: 1,
      name: 'Google',
      industry: 'Technology',
      website: 'https://google.com',
      careers_page: 'https://careers.google.com',
      description: 'Google LLC is an American multinational technology company specializing in artificial intelligence, search engine, online advertising, cloud computing, and computer software.',
      headquarters: 'Mountain View, CA',
      company_size: '10,000+',
      request_count: 8,
      is_active: true
    },
    {
      id: 2,
      name: 'Microsoft',
      industry: 'Software',
      website: 'https://microsoft.com',
      careers_page: 'https://careers.microsoft.com',
      description: 'Microsoft Corporation is an American multinational technology corporation head-quartered in Redmond, Washington. Best known for software like Windows, Office, and Azure.',
      headquarters: 'Redmond, WA',
      company_size: '10,000+',
      request_count: 5,
      is_active: true
    },
    {
      id: 3,
      name: 'Netflix',
      industry: 'Entertainment',
      website: 'https://netflix.com',
      careers_page: 'https://jobs.netflix.com',
      description: 'Netflix, Inc. is an American media company based in Los Gatos, California. Offers subscription-based streaming services with award-winning original shows and movies.',
      headquarters: 'Los Gatos, CA',
      company_size: '5,000 - 10,000',
      request_count: 3,
      is_active: true
    },
    {
      id: 4,
      name: 'Apple',
      industry: 'Hardware & Tech',
      website: 'https://apple.com',
      careers_page: 'https://careers.apple.com',
      description: 'Apple Inc. is an American multinational technology company head-quartered in Cupertino, California. Best known for premium products like iPhone, iPad, Mac, and Apple Watch.',
      headquarters: 'Cupertino, CA',
      company_size: '10,000+',
      request_count: 2,
      is_active: true
    }
  ];

  const companies = rawCompanies.length > 0 ? rawCompanies : mockCompanies;

  const createCompanyMutation = useMutation({
    mutationFn: () => companyApi.create({
      name,
      industry: industry || null,
      website: website || null,
      careers_page: careersPage || null,
      description: description || null,
      headquarters: headquarters || null,
      company_size: companySize || null,
    } as any),
    onSuccess: () => {
      toast.success('New company successfully added to directory!');
      setIsCreateModalOpen(false);
      setName('');
      setIndustry('');
      setWebsite('');
      setCareersPage('');
      setDescription('');
      setHeadquarters('');
      queryClient.invalidateQueries({ queryKey: ['companies-list-main'] });
    },
    onError: () => {
      toast.error('Failed to create company');
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      toast.error('Company Name is required');
      return;
    }
    createCompanyMutation.mutate();
  };

  // Filter companies
  const filteredCompanies = companies.filter((c) => {
    return c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
           (c.industry && c.industry.toLowerCase().includes(searchTerm.toLowerCase()));
  });

  const currentUser = user || { role: 'student' };

  return (
    <div className="space-y-6 animate-fade-in text-slate-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">Companies Directory</h1>
          <p className="text-slate-500 text-xs mt-0.5">Explore active corporations partnered with our AlumniConnect platform</p>
        </div>
        {currentUser.role === 'admin' && (
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-slate-950 font-bold rounded-xl shadow-lg transition-transform hover:scale-[1.02] active:scale-95"
          >
            <Plus className="h-4 w-4 text-slate-950" />
            <span>Add Company</span>
          </button>
        )}
      </div>

      {/* Search Bar */}
      <div className="bg-slate-950 border border-slate-800/80 rounded-2xl p-4 shadow-xl flex items-center gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3.5 top-3 h-4.5 w-4.5 text-slate-500" />
          <input
            type="text"
            placeholder="Search by company name or industry..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 focus:ring-1 focus:ring-sky-500/50 rounded-xl py-2.5 pl-11 pr-4 text-sm text-slate-200 focus:outline-none placeholder-slate-500"
          />
        </div>
      </div>

      {/* Grid of Companies */}
      {isLoading ? (
        <div className="flex justify-center items-center py-24">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-400" />
        </div>
      ) : filteredCompanies.length === 0 ? (
        <div className="bg-slate-950 border border-slate-800/80 rounded-3xl p-12 text-center shadow-xl">
          <HelpCircle className="h-12 w-12 text-slate-600 mx-auto mb-4" />
          <h3 className="font-bold text-slate-300 text-lg">No Companies Registered</h3>
          <p className="text-slate-500 text-xs mt-1">Try another search keyword.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
          {filteredCompanies.map((company) => (
            <div 
              key={company.id}
              className="bg-slate-950 border border-slate-800/80 rounded-2xl p-6 shadow-lg flex flex-col justify-between hover:border-slate-700/60 hover:shadow-2xl transition-all duration-300 group hover:scale-[1.01]"
            >
              <div>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <div className="h-12 w-12 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center text-sky-400 group-hover:text-purple-400 transition-colors">
                      <Building2 className="h-6 w-6" />
                    </div>
                    <div>
                      <h3 className="text-base font-extrabold text-slate-100 group-hover:text-sky-400 transition-colors">
                        {company.name}
                      </h3>
                      {company.industry && (
                        <span className="text-[10px] uppercase font-bold text-purple-400 mt-0.5 tracking-wider bg-purple-500/10 px-2 py-0.5 rounded">
                          {company.industry}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="inline-flex items-center gap-1 text-[10px] text-slate-400 font-bold bg-slate-900 border border-slate-850 px-2 py-1 rounded">
                      <Briefcase className="h-3 w-3" />
                      <span>{company.request_count || 0} Request(s)</span>
                    </span>
                  </div>
                </div>

                <p className="text-xs text-slate-400 mt-4 leading-relaxed line-clamp-3">
                  {company.description || 'No description provided for this company.'}
                </p>

                {/* Company Metadata */}
                <div className="grid grid-cols-2 gap-4 mt-6 pt-4 border-t border-slate-800/50 text-[11px] text-slate-500 font-semibold">
                  <div className="flex items-center gap-1.5">
                    <MapPin className="h-3.5 w-3.5" />
                    <span>{company.headquarters || 'Global HQ'}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Users className="h-3.5 w-3.5" />
                    <span>{company.company_size || '1,000+ employees'}</span>
                  </div>
                </div>
              </div>

              {/* Bottom links */}
              <div className="flex items-center gap-3 mt-6 pt-4 border-t border-slate-800/50">
                {company.website && (
                  <a
                    href={company.website}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-[11px] font-bold text-sky-400 hover:text-sky-300 transition-colors"
                  >
                    <Globe className="h-3.5 w-3.5" />
                    <span>Website</span>
                  </a>
                )}
                {company.careers_page && (
                  <a
                    href={company.careers_page}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-[11px] font-bold text-purple-400 hover:text-purple-300 transition-colors ml-2"
                  >
                    <Briefcase className="h-3.5 w-3.5" />
                    <span>Careers Page</span>
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Admin Add Company Modal */}
      {isCreateModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-md p-4">
          <div className="bg-slate-950 border border-slate-800 rounded-3xl w-full max-w-lg p-6 relative overflow-hidden shadow-2xl animate-fade-in text-slate-200">
            <div className="absolute top-0 right-0 -mt-12 -mr-12 h-36 w-36 rounded-full bg-sky-500/5 blur-2xl" />
            
            <div className="flex items-center justify-between border-b border-slate-800/60 pb-4">
              <h2 className="text-xl font-extrabold flex items-center gap-2">
                <Building2 className="h-5.5 w-5.5 text-sky-400" />
                <span>Register a Company</span>
              </h2>
              <button 
                onClick={() => setIsCreateModalOpen(false)}
                className="p-1 rounded-lg text-slate-400 hover:bg-slate-900"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4 mt-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="label text-xs text-slate-400 uppercase">Company Name *</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Google"
                    className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2 px-3 text-xs text-slate-300 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="label text-xs text-slate-400 uppercase">Industry</label>
                  <input
                    type="text"
                    value={industry}
                    onChange={(e) => setIndustry(e.target.value)}
                    placeholder="e.g. Technology"
                    className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2 px-3 text-xs text-slate-300 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="label text-xs text-slate-400 uppercase">Website URL</label>
                  <input
                    type="text"
                    value={website}
                    onChange={(e) => setWebsite(e.target.value)}
                    placeholder="e.g. https://google.com"
                    className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2 px-3 text-xs text-slate-300 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="label text-xs text-slate-400 uppercase">Careers Page URL</label>
                  <input
                    type="text"
                    value={careersPage}
                    onChange={(e) => setCareersPage(e.target.value)}
                    placeholder="e.g. https://careers.google.com"
                    className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2 px-3 text-xs text-slate-300 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="label text-xs text-slate-400 uppercase">Headquarters</label>
                  <input
                    type="text"
                    value={headquarters}
                    onChange={(e) => setHeadquarters(e.target.value)}
                    placeholder="e.g. Mountain View, CA"
                    className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2 px-3 text-xs text-slate-300 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="label text-xs text-slate-400 uppercase">Company Size</label>
                  <select
                    value={companySize}
                    onChange={(e) => setCompanySize(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2 px-3 text-xs text-slate-300 focus:outline-none"
                  >
                    <option value="1-50">1 - 50 employees</option>
                    <option value="50-250">50 - 250 employees</option>
                    <option value="250-1000">250 - 1000 employees</option>
                    <option value="1000-5000">1000 - 5000 employees</option>
                    <option value="5000-10000">5000 - 10000 employees</option>
                    <option value="10000+">10000+ employees</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="label text-xs text-slate-400 uppercase">Description</label>
                <textarea
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Provide a brief summary of what the company does..."
                  className="w-full bg-slate-900 border border-slate-800 focus:border-sky-500 rounded-xl py-2 px-3 text-xs text-slate-300 focus:outline-none"
                />
              </div>

              <div className="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-slate-800/60">
                <button
                  type="button"
                  onClick={() => setIsCreateModalOpen(false)}
                  className="px-4 py-2 text-xs font-bold text-slate-400 hover:text-slate-200 hover:bg-slate-900 rounded-lg transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createCompanyMutation.isPending}
                  className="inline-flex items-center gap-1.5 px-5 py-2.5 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-slate-950 font-bold rounded-xl transition-all shadow-lg shadow-sky-500/5 disabled:opacity-50 text-xs"
                >
                  <Send className="h-3.5 w-3.5 text-slate-950" />
                  <span>{createCompanyMutation.isPending ? 'Registering...' : 'Register Company'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Companies;
