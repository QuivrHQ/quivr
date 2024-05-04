// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useAuthModes = () => {
  const authModes = process.env.NEXT_PUBLIC_AUTH_MODES?.split(",") ?? [
    "password",
  ];

  return {
    magicLink: authModes.includes("magic_link"),
    password: authModes.includes("password"),
    googleSso: authModes.includes("google_sso"),
  };
};
