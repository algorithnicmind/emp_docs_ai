export interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "hr" | "engineering" | "finance" | "general";
  department: string;
}

export interface Document {
  id: string;
  title: string;
  source: string;
  department: string;
  access_level: "all" | "department" | "confidential";
  status: "processing" | "indexed" | "failed" | "deleted";
  chunk_count: number;
  word_count?: number;
  created_at: string;
}

export interface QueryResponse {
  query_id: string;
  answer: string;
  sources: Source[];
  confidence: "high" | "medium" | "low";
  response_time_ms: number;
  model?: string;
  tokens_used?: number;
  cached?: boolean;
}

export interface Source {
  index: number;
  title: string;
  source: string;
  document_id: string;
  similarity_score: number;
}

export interface Stats {
  total_documents: number;
  total_chunks: number;
  total_queries: number;
  total_users: number;
  avg_feedback_score: number;
  avg_response_time_ms: number;
}
