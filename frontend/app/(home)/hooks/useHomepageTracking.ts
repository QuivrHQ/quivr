import { useRouter } from "next/navigation";
import { MouseEvent } from "react";

import { useEventTracking } from "@/services/analytics/june/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useHomepageTracking = () => {
  const { track } = useEventTracking();
  const router = useRouter();

  const onLinkClick = ({
    href,
    label,
    event,
  }: {
    href: string;
    label: string;
    event: MouseEvent<HTMLAnchorElement>;
  }) => {
    event.preventDefault();
    void track(`HOMEPAGE-${label}`);
    router.push(href);
  };

  const onButtonClick = ({ label }: { label: string }) => {
    void track(`HOMEPAGE-${label}`);
  };

  return {
    onLinkClick,
    onButtonClick,
  };
};
