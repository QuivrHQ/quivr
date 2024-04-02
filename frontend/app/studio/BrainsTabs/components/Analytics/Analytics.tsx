import { useEffect } from "react";

import { useAnalytics } from "@/lib/api/analytics/useAnalyticsApi";

export const Analytics = (): JSX.Element => {
  const { getBrainsUsages } = useAnalytics();

  useEffect(() => {
    void (async () => {
      try {
        const res = await getBrainsUsages();
        console.log(res);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  return <div>Analytics</div>;
};
