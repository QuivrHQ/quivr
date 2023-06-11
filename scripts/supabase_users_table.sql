create table if not exists users(
    user_id uuid primary key,
    email text,
    date text,
    requests_count int
);
