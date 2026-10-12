-- The worker starts conservative clocks in bounded pages, including old rows.
-- Nullable additions let previous writers omit them without a backfill.
ALTER TABLE matches ADD COLUMN retention_started_at timestamptz;
ALTER TABLE monitoring_notices ADD COLUMN retention_started_at timestamptz;
ALTER TABLE evaluation_intents ADD COLUMN retention_started_at timestamptz;

-- The application creates checkpoint rows when it first runs each stage.
CREATE TABLE history_retention_progress (
 kind text PRIMARY KEY,
 cursor jsonb NOT NULL DEFAULT '[]'
);
