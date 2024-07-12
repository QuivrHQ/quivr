alter table "public"."knowledge" add column "status" text not null default 'UPLOADED'::text;

CREATE UNIQUE INDEX knowledge_pkey ON public.knowledge USING btree (id);

alter table "public"."knowledge" add constraint "knowledge_pkey" PRIMARY KEY using index "knowledge_pkey";


