import ReactGA from "react-ga4";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useGAnalyticsEventTracker = ({
  category,
}: {
  category: string;
}) => {
  const ga_id = process.env.NEXT_PUBLIC_GA_ID;

  if (ga_id === undefined) {
    return { eventTracker: undefined };
  }

  ReactGA.initialize(ga_id);

  const eventTracker = ({
    action,
    label,
  }: {
    action: string;
    label?: string;
  }) => {
    ReactGA.event(action, {
      category,
      label,
    });
  };

  return { eventTracker };
};
