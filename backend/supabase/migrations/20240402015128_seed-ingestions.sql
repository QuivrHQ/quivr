INSERT INTO "public"."ingestions" ("name", "id", "brain_id_required", "file_1_required", "url_required")
SELECT 'summary', 'bc414385-342e-49fc-b252-3529c935c63a', true, true, false
WHERE NOT EXISTS (
    SELECT 1 FROM "public"."ingestions" WHERE "id" = 'bc414385-342e-49fc-b252-3529c935c63a'
);

INSERT INTO "public"."ingestions" ("name", "id", "brain_id_required", "file_1_required", "url_required")
SELECT 'audio_transcript', 'c502a10d-5a98-40f9-9699-a65d7ece37de', true, true, false
WHERE NOT EXISTS (
    SELECT 1 FROM "public"."ingestions" WHERE "id" = 'c502a10d-5a98-40f9-9699-a65d7ece37de'
);

INSERT INTO "public"."ingestions" ("name", "id", "brain_id_required", "file_1_required", "url_required")
SELECT 'crawler', '948ae685-5710-4dde-bb80-36ce0097ca7b', true, false, true
WHERE NOT EXISTS (
    SELECT 1 FROM "public"."ingestions" WHERE "id" = '948ae685-5710-4dde-bb80-36ce0097ca7b'
);
