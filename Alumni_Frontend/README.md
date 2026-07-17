# AlumniConnect — Frontend (`Alumni_Frontend`)

React + TypeScript client for the AlumniConnect placement referral platform, with role-specific dashboards, a typed REST API layer, and protected routing.

> Part of the [AlumniConnect monorepo](../README.md). Requires the [backend](../Alumni_Project_Final/README.md) running on `http://localhost:8000`.

## Features

- Role-based dashboards (Student / Alumni / Admin)
- Auth flow: login, register, email verification
- Referral request management — create, edit, submit, track status
- Company directory with search
- Admin panel for approving/rejecting requests
- Typed REST API client with automatic token refresh on 401
- Form validation via React Hook Form + Zod schemas
- Responsive layout (mobile, tablet, desktop)

## Tech Stack

| | |
|---|---|
| Framework | React 18, TypeScript, Vite |
| Styling | TailwindCSS |
| Routing | React Router v6 |
| Server state | React Query |
| Global state | Zustand |
| HTTP client | Axios (with interceptors for auth refresh) |
| Forms | React Hook Form + Zod |
| Icons | Lucide Icons |
| Notifications | React Hot Toast |

## Getting Started

### Prerequisites
- Node.js 18+
- Backend running on `http://localhost:8000` (see [backend README](../Alumni_Project_Final/README.md))

### Installation

```bash
cd Alumni_Frontend
npm install
cp .env.example .env
npm run dev
```

App runs at `http://localhost:3000`.

### Environment variables

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Authentication Flow

- On login, the backend returns an access token and a refresh token; both are stored via Zustand (persisted) and attached to requests by an Axios interceptor
- On a 401 response, the interceptor attempts a token refresh and retries the original request; if refresh fails, the user is logged out and redirected
- Protected routes check `isAuthenticated` and the user's role before rendering, redirecting unauthorized users

## Project Structure

```
src/
├── components/
│   ├── ui/              # Button, Card, Badge, Input, Select, Modal, Table, Tabs
│   ├── forms/
│   └── layouts/
├── pages/
│   ├── auth/             # Login, Register
│   ├── admin/             # Admin panel
│   ├── Dashboard.tsx
│   ├── ReferralRequests.tsx
│   ├── CreateRequest.tsx
│   ├── RequestDetail.tsx
│   └── Companies.tsx
├── services/              # API service layer (auth, referral-request, company, admin)
├── store/                  # Zustand stores (auth.ts)
├── hooks/                   # custom hooks
├── types/                    # TypeScript types
├── lib/                       # api-client.ts and other configs
├── App.tsx
└── main.tsx
```

## Pages

| Page | Role | Purpose |
|---|---|---|
| Dashboard | All | Stats, recent activity, role-specific quick actions |
| Referral Requests | Student | Create/track referral requests |
| Companies | All | Browse/search company directory |
| Admin Panel | Admin | Approve/reject pending requests, view system stats |
| Profile | All | Edit profile, change password, verification status |

## UI Component Conventions

```tsx
<Button variant="primary" size="md">Click me</Button>

<Card>
  <CardHeader>Title</CardHeader>
  <CardContent>Content</CardContent>
</Card>

<Badge variant="success">Approved</Badge>

<Input label="Email" type="email" {...register('email')} />
```

Forms use React Hook Form with Zod resolvers:
```tsx
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const { register, handleSubmit } = useForm({
  resolver: zodResolver(schema),
});
```

## Design System

| Token | Value |
|---|---|
| Primary | `#0ea5e9` |
| Secondary | `#a855f7` |
| Success | `#10b981` |
| Warning | `#f59e0b` |
| Error | `#ef4444` |
| Font | Inter (system font fallback) |

### Breakpoints (Tailwind defaults)
`sm` 640px · `md` 768px · `lg` 1024px · `xl` 1280px · `2xl` 1536px

## Build

```bash
npm run build     # outputs to dist/
```

## Roadmap

Ideas for future iterations — not yet built:
- Dark mode
- Advanced multi-criteria filtering on referral requests
- CSV/PDF export of request history

## License

MIT
