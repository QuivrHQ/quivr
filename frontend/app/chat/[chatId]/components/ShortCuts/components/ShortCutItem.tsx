type ShortcutItemProps = {
  content: string[];
};

export const ShortcutItem = ({ content }: ShortcutItemProps): JSX.Element => {
  return (
    <div className="bg-gray-100 rounded-lg p-4 flex-grow">
      {content.map((text, index) => (
        <p className="text-gray-500" key={index}>
          {text}
        </p>
      ))}
    </div>
  );
};
