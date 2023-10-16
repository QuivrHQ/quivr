import { CasesList } from "./components/CasesList/CasesList";

export const UseCases = (): JSX.Element => {
  return (
    <section className="p-4 bg-purple-800 text-white">
      <div className="mb-3">
        <h2 className="text-center text-3xl font-semibold mb-2">
          Experience it now.
        </h2>
        <p className="text-center text-lg">Check our example on using Quivr</p>
      </div>
      <CasesList />
    </section>
  );
};
