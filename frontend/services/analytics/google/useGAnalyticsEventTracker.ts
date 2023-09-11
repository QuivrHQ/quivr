import { event, initialize } from "react-ga";
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useGAnalyticsEventTracker = (category: string) => {
  const ga_id = process.env.NEXT_PUBLIC_GA_ID;

  if (ga_id === undefined) {
    return undefined;
  }

  initialize(ga_id);

  const eventTracker = ({
    action,
    label,
  }: {
    action: string;
    label?: string;
  }) => {
    event({ category, action, label });
  };

  return eventTracker;
};
