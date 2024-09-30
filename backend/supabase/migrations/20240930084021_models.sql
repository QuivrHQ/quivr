-- Rename the column
ALTER TABLE "public"."models" RENAME COLUMN "max_input" TO "max_context_tokens";

-- Set the default value for the renamed column
ALTER TABLE "public"."models" ALTER COLUMN "max_context_tokens" SET DEFAULT 4000;

-- Add a description to the renamed column
COMMENT ON COLUMN "public"."models"."max_context_tokens" IS 'Maximum number of tokens passed to the LLM as a context to generate the answer.';
