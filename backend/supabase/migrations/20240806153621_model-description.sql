alter table "public"."models" add column "description" text not null default 'Default Description'::text;

alter table "public"."models" add column "display_name" text not null default gen_random_uuid();

alter table "public"."models" add column "image_url" text not null default 'https://quivr-cms.s3.eu-west-3.amazonaws.com/logo_quivr_white_7e3c72620f.png'::text;
