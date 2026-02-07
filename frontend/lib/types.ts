// Type definitions matching backend API responses (snake_case)

export interface User {
  id: string;
  email: string;
  created_at?: string;
  updated_at?: string;
}

export interface UserSession {
  user: User;
  token: string;
  expiresAt?: string;
}

export interface TodoItem {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  user_id: string;
  created_at: string;
  updated_at?: string;
}

export interface TodoCreateData {
  title: string;
  description?: string;
  is_completed?: boolean;
}

export interface TodoUpdateData {
  title?: string;
  description?: string;
  is_completed?: boolean;
}
