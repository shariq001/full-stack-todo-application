import { NextRequest, NextResponse } from 'next/server';
import { betterAuth } from 'better-auth';
import { Pool, neonConfig } from '@neondatabase/serverless';
import ws from 'ws';

// Enable WebSocket for serverless environments (Vercel)
neonConfig.webSocketConstructor = ws;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Get the base URL from environment or construct from request
const getBaseURL = (request?: NextRequest): string => {
  // Use env var if explicitly set
  if (process.env.NEXT_PUBLIC_BETTER_AUTH_URL) {
    return process.env.NEXT_PUBLIC_BETTER_AUTH_URL;
  }

  // Try to get from request headers
  if (request) {
    const host = request.headers.get('x-forwarded-host') || request.headers.get('host');
    const proto = request.headers.get('x-forwarded-proto') || 'http';
    if (host) {
      return `${proto}://${host}`;
    }
  }

  // Fallback
  return "http://localhost:3000";
};

// Create a function to initialize auth with the correct base URL
const createAuth = (baseURL: string) => betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL,
  database: pool,
  session: {
    expiresIn: 60 * 60 * 24,
    updateAge: 60 * 60,
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
});

export async function GET(request: NextRequest) {
  try {
    const baseURL = getBaseURL(request);
    const auth = createAuth(baseURL);
    return await auth.handler(request);
  } catch (error: any) {
    console.error('[Auth GET Error]', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const baseURL = getBaseURL(request);
    const auth = createAuth(baseURL);
    return await auth.handler(request);
  } catch (error: any) {
    console.error('[Auth POST Error]', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
