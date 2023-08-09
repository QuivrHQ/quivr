type StyleMentionsInputProps = {
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
};

export const MentionsInput = ({
  onChange,
  placeholder,
  value,
}: StyleMentionsInputProps): JSX.Element => {
  return (
    <input
      autoFocus
      placeholder={placeholder}
      onChange={(event) => onChange(event.target.value)}
      value={value}
      className="focus:outline-none focus:border-none"
    />
  );
};
