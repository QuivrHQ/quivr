import { EntryComponentProps } from "@draft-js-plugins/mention/lib/MentionSuggestions/Entry/Entry";
import { ComponentType, useEffect, useRef } from "react";

export const withCustomEntryComponent = <
  P extends EntryComponentProps & { isFocused: boolean }
>(
  WrappedComponent: ComponentType<P>
): ComponentType<P> => {
  const EnrichedBrainSuggestion = (props: P) => {
    const entryRef = useRef(null);
    let className = "mention-text";

    if (props.isFocused) {
      className += " mention-focused";
    }

    useEffect(() => {
      if (props.isFocused) {
        if ("scrollIntoViewIfNeeded" in document.body) {
          entryRef.current?.scrollIntoViewIfNeeded?.(false);
        } else {
          entryRef.current?.scrollIntoView?.(false);
        }
      }
    }, [props.isFocused]);

    return (
      <div ref={entryRef} className={className}>
        <WrappedComponent {...props} />
      </div>
    );
  };

  EnrichedBrainSuggestion.displayName = `withEnrichedBrainSuggestion`;

  return EnrichedBrainSuggestion;
};
