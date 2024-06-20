create type "public"."tags" as enum ('Finance', 'Legal', 'Health', 'Technology', 'Education', 'Resources', 'Marketing', 'Strategy', 'Operations', 'Compliance', 'Research', 'Innovation', 'Sustainability', 'Management', 'Communication', 'Data', 'Quality', 'Logistics', 'Policy', 'Design', 'Safety', 'Customer', 'Development', 'Reporting', 'Collaboration');

alter table "public"."brains" add column "tags" tags[];
