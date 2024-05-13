alter table "public"."brains" drop constraint "brains_prompt_id_fkey";

alter table "public"."chat_history" drop constraint "chat_history_prompt_id_fkey";

alter table "public"."brains" add constraint "brains_prompt_id_fkey" FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."brains" validate constraint "brains_prompt_id_fkey";

alter table "public"."chat_history" add constraint "chat_history_prompt_id_fkey" FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."chat_history" validate constraint "chat_history_prompt_id_fkey";

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
    (bu.user_id = p_user_id AND bu.rights IN ('Owner', 'Editor', 'Viewer'))
  ORDER BY
    b.meaning <=> query_embedding
  LIMIT
    match_count;
END;
$function$
;


