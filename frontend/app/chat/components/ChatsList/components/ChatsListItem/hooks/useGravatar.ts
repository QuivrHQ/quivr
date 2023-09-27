import { createHash } from "crypto";
import { useEffect, useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";

// Gravatar images may be requested just like a normal image, using an IMG tag. To get an image specific to a user, you must first calculate their email hash.
// The most basic image request URL looks like this:
// https://www.gravatar.com/avatar/HASH

const computeGravatarUrl = (email?: string) => {
  const hash = createHash("md5")
    .update(typeof email === "string" ? email.trim().toLowerCase() : "")
    .digest("hex");

  return `https://www.gravatar.com/avatar/${hash}?d=mp`;
};

export const useGravatar = (): { gravatarUrl: string } => {
  const { session } = useSupabase();
  const [gravatarUrl, setGravatarUrl] = useState<string>(computeGravatarUrl());

  const email = session?.user.email;

  useEffect(() => {
    const computedUrl = computeGravatarUrl(email);
    setGravatarUrl(computedUrl);
  }, [email]);

  return { gravatarUrl };
};
