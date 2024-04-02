alter table "public"."ingestions" add column "brain_id_required" boolean not null default true;

alter table "public"."ingestions" add column "file_1_required" boolean not null default false;


