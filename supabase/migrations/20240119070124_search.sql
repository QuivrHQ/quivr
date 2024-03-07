alter table "public"."brains" add column "meaning" vector;

alter table "public"."brains" alter column "description" set default 'This needs to be changed'::text;

alter table "public"."brains" alter column "description" set not null;

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.match_brain(query_embedding vector, match_count integer)
 RETURNS TABLE(id uuid, name text, similarity double precision)
 LANGUAGE plpgsql
AS $function$
#variable_conflict use_column
begin
  return query
  select
    brain_id,
    name,
    1 - (brains.meaning <=> query_embedding) as similarity
  from brains
  order by brains.meaning <=> query_embedding
  limit match_count;
end;
$function$
;


