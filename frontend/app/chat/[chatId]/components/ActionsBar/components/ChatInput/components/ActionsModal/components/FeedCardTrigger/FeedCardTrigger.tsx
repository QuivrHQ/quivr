import { LuChevronRight } from "react-icons/lu";

import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import { useFeedCardTrigger } from "./hooks/useFeedCardTrigger";
import { Button } from "../Button";

export const FeedCardTrigger = (): JSX.Element => {
  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();
  const { label, Icon } = useFeedCardTrigger();

  return (
    <Button
      label={label}
      startIcon={<Icon size={18} />}
      endIcon={<LuChevronRight size={18} />}
      className="w-full"
      onClick={() => setShouldDisplayFeedCard(true)}
    />
  );
};
