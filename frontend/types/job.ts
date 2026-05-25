export interface Job {
  id: string;
  title: string;
  company: string;
  location?: string | null;
  description: string;
  url: string;
  source: string;
  saved: boolean;
  salary_min?: number;
  salary_max?: number;
  currency?: string;
  scraped_at?: string;
  relevance_score?: number | null;
  embedding_status: 'pending' | 'processing' | 'ready';
  similarity_score?: number | null;
  recruiter_id?: string | null;
}
