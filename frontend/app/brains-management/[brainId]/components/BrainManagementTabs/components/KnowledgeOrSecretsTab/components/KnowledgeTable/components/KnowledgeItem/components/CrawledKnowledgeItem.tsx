"use client";

export const CrawledKnowledgeItem = ({ url }: { url: string }): JSX.Element => {
  return (
    <a href={url} target="_blank" rel="noopener noreferrer">
      <div className="text-sm text-gray-900">
        <p className={"max-w-[400px] truncate"}>{url}</p>
      </div>
    </a>
  );
};
