type ColoredTextProps = {
  color: string;
  text: string;
  className?: string;
};

// color should be a valid tailwind class
export const ColoredText = ({
  color,
  text,
  className = "",
}: ColoredTextProps): JSX.Element => (
  <span className={`${className} ${color}`}>{text}</span>
);
