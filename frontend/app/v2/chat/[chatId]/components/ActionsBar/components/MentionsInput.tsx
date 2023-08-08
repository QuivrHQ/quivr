import {
  MentionProps,
  MentionsInput as ReactMentionsInput,
} from "react-mentions";

type StyleMentionsInputProps = {
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  children:
    | React.ReactElement<MentionProps>
    | Array<React.ReactElement<MentionProps>>;
  disabled?: boolean;
};

export const MentionsInput = ({
  children,
  onChange,
  placeholder,
  value,
  disabled = false,
}: StyleMentionsInputProps): JSX.Element => {
  if (disabled) {
    return (
      <input
        autoFocus
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
        value={value}
        className="focus:outline-none focus:border-none"
      />
    );
  }

  return (
    <ReactMentionsInput
      placeholder={placeholder}
      value={value}
      autoFocus
      onChange={(_, __, newValue) => onChange(newValue)}
      forceSuggestionsAboveCursor
      style={{
        input: {
          outline: "none",
          border: "none",
          "&:focus": {
            outline: "none",
            border: "none",
          },
        },
        suggestions: {
          zIndex: 99999,
          boxShadow:
            "0px 4px 6px rgba(0, 0, 0, 0.1), 0px 2px 4px rgba(0, 0, 0, 0.06)",
          "@media (prefers-color-scheme: dark)": {
            boxShadow:
              "0px 4px 6px rgba(255, 255, 255, 0.25), 0px 2px 4px rgba(255, 255, 255, 0.125)",
          },
          "&:hover": {
            boxShadow:
              "0px 10px 15px rgba(0, 0, 0, 0.1), 0px 4px 6px rgba(0, 0, 0, 0.06)",
          },
          transition: "box-shadow 0.3s ease",
          borderRadius: "0.75rem",
          background: "white",
          border: "1px solid rgba(0, 0, 0, 0.1)",
          padding: "1.5rem",
        },
      }}
    >
      {children}
    </ReactMentionsInput>
  );
};
