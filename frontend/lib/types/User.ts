export type RequestStat = {
  date: string;
  daily_requests_count: number;
  user_id: string;
};

export interface UserStats {
  email: string;
  max_brain_size: number;
  current_brain_size: number;
  daily_chat_credit: number;
  requests_stats: RequestStat[];
  date: string;
  models: string[];
  is_premium: boolean;
}
