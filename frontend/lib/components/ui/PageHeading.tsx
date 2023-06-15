interface PageHeadingProps {
  title: string;
  subtitle?: string;
}

const PageHeading = ({ title, subtitle }: PageHeadingProps): JSX.Element => {
  return (
    <div className="flex flex-col items-center justify-center px-5">
      <h1 className="text-3xl font-bold text-center">{title}</h1>
      {subtitle !== undefined && (
        <h2 className="opacity-50 text-center">{subtitle}</h2>
      )}
    </div>
  );
};

export default PageHeading;
