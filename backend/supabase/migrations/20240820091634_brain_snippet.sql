alter table "public"."brains" add column "snippet_color" text not null default '#d0c6f2'::text;

alter table "public"."brains" add column "snippet_emoji" text not null default '🧠'::text;


