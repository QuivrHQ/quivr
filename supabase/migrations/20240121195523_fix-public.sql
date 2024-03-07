create type "public"."thumbs" as enum ('up', 'down');

drop function if exists "public"."match_brain"(query_embedding vector, match_count integer);

alter table "public"."chat_history" add column "user_feedback" thumbs;

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.match_brain(query_embedding vector, match_count integer, p_user_id uuid)
 RETURNS TABLE(id uuid, name text, similarity double precision)
 LANGUAGE plpgsql
AS $function$
BEGIN
  RETURN QUERY
  SELECT
    b.brain_id,
    b.name,
    1 - (b.meaning <=> query_embedding) as similarity
  FROM
    brains b
  LEFT JOIN
    brains_users bu ON b.brain_id = bu.brain_id
  WHERE
    (b.status = 'public') OR 
    (bu.user_id = p_user_id AND bu.rights IN ('Owner', 'Editor', 'Viewer'))
  ORDER BY
    b.meaning <=> query_embedding
  LIMIT
    match_count;
END;
$function$
;


