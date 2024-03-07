import * as Sentry from "@sentry/nextjs";

// Get the DSN from the environment variable
const SENTRY_DSN = process.env.NEXT_PUBLIC_SENTRY_DSN;

// Only initialize Sentry if the DSN is set
if (SENTRY_DSN) {
  Sentry.init({
    dsn: SENTRY_DSN,

    // Adjust this value in production, or use tracesSampler for greater control
    tracesSampleRate: 0.1,
    sampleRate: 0.1,

    // Setting this option to true will print useful information to the console while you're setting up Sentry.
    debug: false,
  });
} else {
  console.log(
    "Sentry is not initialized on the server as SENTRY_DSN is not set"
  );
}
