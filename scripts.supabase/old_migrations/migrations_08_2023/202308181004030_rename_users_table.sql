-- Create a new user_daily_usage table
create table if not exists
  user_daily_usage (
    user_id uuid references auth.users (id),
    email text,
    date text,
    daily_requests_count int,
    primary key (user_id, date)
  );

-- Drop the old users table
drop table if exists users;

-- Update migrations table
insert into
  migrations (name)
select
  '202308181004030_rename_users_table'
where
  not exists (
    select
      1
    from
      migrations
    where
      name = '202308181004030_rename_users_table'
  );

commit;