import { createAuthClient } from "better-auth/client";

// Get the auth URL based on environment
const getAuthBaseURL = () => {
  // If explicitly set via env var, use it
  if (process.env.NEXT_PUBLIC_BETTER_AUTH_URL) {
    return process.env.NEXT_PUBLIC_BETTER_AUTH_URL;
  }

  // Client-side: use current domain
  if (typeof window !== "undefined") {
    return window.location.origin;
  }

  // Server-side fallback
  return "http://localhost:3000";
};

const authClient = createAuthClient({
  baseURL: getAuthBaseURL(),
});

export default authClient;
export { authClient };
