# Quickstart Guide: Frontend Reset & Next.js Initialization

**Date**: 2026-02-06
**Feature**: Frontend Reset & Proper Next.js Initialization
**Branch**: 004-frontend-reset

## Overview

This guide provides instructions for setting up the properly initialized Next.js frontend for the task management application. This document assumes the frontend has been reset and initialized using the official Next.js tooling with App Router.

## Prerequisites

- Node.js 18.x or higher
- npm or yarn package manager
- Git
- Access to the project repository

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Navigate to Frontend Directory

```bash
cd frontend
```

### 3. Install Dependencies

```bash
npm install
# or
yarn install
```

### 4. Environment Configuration

Create a `.env.local` file in the frontend directory with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-key
```

### 5. Running the Development Server

```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## Project Structure

After initialization, the project follows this structure:

```
frontend/
├── app/                 # App Router pages and layouts
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page
│   ├── globals.css      # Global styles
│   └── ...
├── components/          # Reusable React components
│   ├── ui/              # Basic UI components
│   ├── layout/          # Layout components
│   └── ...
├── lib/                 # Utility functions and services
├── public/              # Static assets
├── next.config.js       # Next.js configuration
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
└── .env.local           # Environment variables
```

## Key Features

### App Router
- File-based routing system in the `app/` directory
- Layouts and templates for shared UI
- Built-in data fetching capabilities
- Streaming and suspense support

### Development Features
- Hot Module Replacement (HMR) during development
- Fast Refresh for quick iteration
- TypeScript support out of the box
- ESLint and Prettier configured

### Styling
- Tailwind CSS for utility-first styling
- CSS Modules support
- Global styles in `app/globals.css`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production build
- `npm run lint` - Run linter
- `npm run type-check` - Run TypeScript checker

## Next Steps

After the frontend is properly initialized:

1. Implement authentication components (following Spec 1 requirements)
2. Create task management components (following Spec 2 requirements)
3. Set up API integration with the backend
4. Implement responsive design and accessibility features
5. Add testing infrastructure

## Troubleshooting

### Common Issues

**Issue**: Module not found errors after installation
**Solution**: Clear cache and reinstall
```bash
rm -rf node_modules package-lock.json
npm install
```

**Issue**: Port already in use
**Solution**: Change port in package.json or kill the process using the port
```bash
npm run dev -- -p 3001
```

**Issue**: Environment variables not loading
**Solution**: Ensure `.env.local` is in the root of the frontend directory and properly formatted

## API Integration

The frontend is prepared to connect to the backend API. The API endpoints will follow the pattern:
- Base URL: `NEXT_PUBLIC_API_BASE_URL` from environment
- Authentication: JWT tokens in Authorization header
- Endpoints: `/api/{user_id}/tasks` for task operations

## Testing

To run tests (once implemented):
```bash
npm run test
# or for watching changes
npm run test:watch
```

## Deployment

For deployment, ensure:
- Environment variables are set in your hosting environment
- Build process completes successfully with `npm run build`
- Static assets are properly served
- API endpoints are correctly configured for the deployment environment