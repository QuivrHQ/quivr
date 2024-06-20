alter table "public"."vectors" alter column "embedding" set not null;

alter table "public"."vectors" alter column "embedding" set data type vector using "embedding"::vector;
