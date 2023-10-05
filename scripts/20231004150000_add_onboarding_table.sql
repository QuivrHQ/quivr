-- Create the onboarding table
CREATE TABLE IF NOT EXISTS onboardings (
  user_id UUID NOT NULL REFERENCES auth.users (id),
  onboarding_b1 BOOLEAN NOT NULL DEFAULT false,
  onboarding_b2 BOOLEAN NOT NULL DEFAULT false,
  onboarding_b3 BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY (user_id)
)