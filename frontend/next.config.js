/* eslint-disable max-lines */
const nextConfig = {
  output: "standalone",
  redirects: async () => {
    return [
      {
        source: "/brains-management/library",
        destination: "/library",
        permanent: false,
      },
    ];
  },
  images: {
    domains: [
      "www.quivr.app",
      "quivr-cms.s3.eu-west-3.amazonaws.com",
      "www.gravatar.com",
      "media.licdn.com",
      "*",
    ],
  },
  // eslint-disable-next-line prefer-arrow/prefer-arrow-functions
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: securityHeaders,
      },
    ];
  },
};

const ContentSecurityPolicy = {
  "default-src": [
    "'self'",
    "https://fonts.googleapis.com",
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    "https://api.june.so",
    "https://us.posthog.com",
    "https://preview.quivr.app",
    "https://*.vercel.app",
    process.env.NEXT_PUBLIC_FRONTEND_URL,
  ],
  "connect-src": [
    "'self'",
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_BACKEND_URL,
    process.env.NEXT_PUBLIC_CMS_URL,
    "https://api.june.so",
    "https://api.openai.com",
    "https://cdn.growthbook.io",
    "https://vitals.vercel-insights.com/v1/vitals",
    "https://us.posthog.com",
  ],
  "img-src": [
    "'self'",
    "https://www.gravatar.com",
    "https://quivr-cms.s3.eu-west-3.amazonaws.com",
    "data:",
    "*",
  ],
  "media-src": [
    "'self'",
    "https://user-images.githubusercontent.com",
    process.env.NEXT_PUBLIC_FRONTEND_URL,
    "https://quivr-cms.s3.eu-west-3.amazonaws.com",
    "https://preview.quivr.app",
    "https://*.vercel.app",
  ],
  "script-src": [
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://va.vercel-scripts.com/",
    process.env.NEXT_PUBLIC_FRONTEND_URL,
    "https://preview.quivr.app",
    "https://*.vercel.app",
    "https://www.google-analytics.com/",
    "https://js.stripe.com",
    "https://us.posthog.com",
  ],
  "frame-src": ["https://js.stripe.com", "https://us.posthog.com"],
  "frame-ancestors": ["'none'"],
  "style-src": [
    "'unsafe-inline'",
    process.env.NEXT_PUBLIC_FRONTEND_URL,
    "https://preview.quivr.app",
    "https://*.vercel.app",
  ],
};

// Build CSP string
const cspString = Object.entries(ContentSecurityPolicy)
  .map(([key, values]) => `${key} ${values.join(" ")};`)
  .join(" ");

// Define headers
const securityHeaders = [
  {
    key: "Content-Security-Policy",
    value: cspString,
  },
  {
    key: "Referrer-Policy",
    value: "origin-when-cross-origin",
  },
  {
    key: "X-Frame-Options",
    value: "SAMEORIGIN",
  },
  {
    key: "X-Content-Type-Options",
    value: "nosniff",
  },
  {
    key: "X-DNS-Prefetch-Control",
    value: "on",
  },
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=(), interest-cohort=()",
  },
  {
    key: "Strict-Transport-Security",
    value: "max-age=31536000",
  },
];
//AJouter le content security policy uniquement en pre-vew et en prod

// Check if the SENTRY_DSN environment variable is defined
if (process.env.SENTRY_DSN) {
  // SENTRY_DSN exists, include Sentry configuration
  const { withSentryConfig } = require("@sentry/nextjs");

  module.exports = withSentryConfig(
    nextConfig,
    {
      // For all available options, see:
      // https://github.com/getsentry/sentry-webpack-plugin#options

      // Suppresses source map uploading logs during build
      silent: true,

      org: "quivr-0f",
      project: "javascript-nextjs",
    },
    {
      // For all available options, see:
      // https://docs.sentry.io/platforms/javascript/guides/nextjs/manual-setup/

      // Upload a larger set of source maps for prettier stack traces (increases build time)
      widenClientFileUpload: true,

      // Transpiles SDK to be compatible with IE11 (increases bundle size)
      transpileClientSDK: true,

      // Routes browser requests to Sentry through a Next.js rewrite to circumvent ad-blockers (increases server load)
      tunnelRoute: "/monitoring",

      // Hides source maps from generated client bundles
      hideSourceMaps: true,

      // Automatically tree-shake Sentry logger statements to reduce bundle size
      disableLogger: true,
    }
  );
} else {
  // SENTRY_DSN does not exist, export nextConfig without Sentry
  module.exports = nextConfig;
}
