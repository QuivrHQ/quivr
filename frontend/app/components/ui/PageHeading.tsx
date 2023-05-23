import { FC } from "react";

interface PageHeadingProps {
  title: string;
  subtitle?: string;
}

const PageHeading: FC<PageHeadingProps> = ({ title, subtitle }) => {
  return (
    <div className="flex flex-col items-center justify-center mt-10">
      <h1 className="text-3xl font-bold text-center">{title}</h1>
      {subtitle && <h2 className="opacity-50">{subtitle}</h2>}
    </div>
  );
};

export default PageHeading;
