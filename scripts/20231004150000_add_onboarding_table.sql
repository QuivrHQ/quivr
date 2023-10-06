-- Create the onboarding table
CREATE TABLE IF NOT EXISTS onboardings (
  user_id UUID NOT NULL REFERENCES auth.users (id),
  onboarding_b1 BOOLEAN NOT NULL DEFAULT true,
  onboarding_b2 BOOLEAN NOT NULL DEFAULT true,
  onboarding_b3 BOOLEAN NOT NULL DEFAULT true,
  PRIMARY KEY (user_id)
)