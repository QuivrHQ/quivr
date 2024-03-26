create type "public"."user_identity_company_size" as enum ('1-10', '10-25', '25-50', '50-100', '100-250', '250-500', '500-1000', '1000-5000', '+5000');

alter table "public"."user_identity" add column "company_size" user_identity_company_size;

alter table "public"."user_identity" add column "role_in_company" text;


