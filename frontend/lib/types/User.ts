export type RequestStat = {
  date: string;
  requests_count: number;
  user_id: string;
};

export interface UserStats {
  email: string;
  max_brain_size: number;
  current_brain_size: number;
  max_requests_number: number;
  requests_stats: RequestStat[];
  date: string;
}
