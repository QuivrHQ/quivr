alter table "public"."models" add column "default" boolean not null default false;

alter table "public"."models" add column "endpoint_url" text not null default 'https://api.openai.com/v1/models'::text;

alter table "public"."models" add column "env_variable_name" text not null default 'OPENAI_API_KEY'::text;

alter table "public"."user_settings" drop column "models";


