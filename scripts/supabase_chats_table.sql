create table if not exists chats(
    chat_id uuid default uuid_generate_v4() primary key,
    user_id uuid references users(user_id),
    creation_time timestamp default current_timestamp,
    history jsonb,
    chat_name text
);