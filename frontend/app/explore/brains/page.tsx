"use client";
import PageHeading from "@/app/components/ui/PageHeading";
import { useBrainScope } from "@/lib/context/BrainScopeProvider/hooks/useBrainScope";
import { FC } from "react";
import BrainListItem from "./components/BrainListItem";

interface BrainsPageProps {}

const BrainsPage: FC<BrainsPageProps> = ({}) => {
  const { allBrains } = useBrainScope();
  return (
    <main>
      <section className="w-full outline-none pt-10 flex flex-col gap-5 items-center justify-center p-6">
        <PageHeading title="Your Brains" subtitle="View and tune your brains" />
        {allBrains.map((brain) => {
          return <BrainListItem brain={brain} />;
        })}
        <div></div>
      </section>
    </main>
  );
};

export default BrainsPage;
