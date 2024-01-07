-- create table "public"."models" (
--     "name" text not null,
--     "price" integer default 1,
--     "max_input" integer default 2000,
--     "max_output" integer default 1000
-- );
CREATE TABLE IF NOT EXISTS public.models (
    name text NOT NULL,
    price integer DEFAULT 1,
    max_input integer DEFAULT 2000,
    max_output integer DEFAULT 1000
);

CREATE UNIQUE INDEX models_pkey ON public.models USING btree (name);

-- alter table "public"."models" add constraint "models_pkey" PRIMARY KEY using index "models_pkey";
ALTER TABLE IF EXISTS public.models ADD CONSTRAINT models_pkey PRIMARY KEY USING INDEX models_pkey;

grant delete on table "public"."models" to "anon";

grant insert on table "public"."models" to "anon";

grant references on table "public"."models" to "anon";

grant select on table "public"."models" to "anon";

grant trigger on table "public"."models" to "anon";

grant truncate on table "public"."models" to "anon";

grant update on table "public"."models" to "anon";

grant delete on table "public"."models" to "authenticated";

grant insert on table "public"."models" to "authenticated";

grant references on table "public"."models" to "authenticated";

grant select on table "public"."models" to "authenticated";

grant trigger on table "public"."models" to "authenticated";

grant truncate on table "public"."models" to "authenticated";

grant update on table "public"."models" to "authenticated";

grant delete on table "public"."models" to "service_role";

grant insert on table "public"."models" to "service_role";

grant references on table "public"."models" to "service_role";

grant select on table "public"."models" to "service_role";

grant trigger on table "public"."models" to "service_role";

grant truncate on table "public"."models" to "service_role";

grant update on table "public"."models" to "service_role";

INSERT INTO public.models ("name", "price", "max_input", "max_output") VALUES
	('gpt-3.5-turbo-1106', 1, 2000, 1000),
  ('gpt-4', 1, 2000, 1000),
  ('gpt-4-1106-preview', 1, 2000, 1000);

-- Update migrations table
INSERT INTO migrations (name)
SELECT '20240103234423_models'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20240103234423_models'
);

COMMIT;
