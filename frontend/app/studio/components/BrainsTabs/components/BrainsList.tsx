import {
  MaterialReactTable,
  useMaterialReactTable,
  // eslint-disable-next-line sort-imports
  type MRT_ColumnDef,
} from "material-react-table";
import { useMemo } from "react";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import { BrainItem } from "./BrainItem";

type BrainsListProps = {
  brains: MinimalBrainForUser[];
};

export const BrainsList = ({ brains }: BrainsListProps): JSX.Element => {
  const columns = useMemo<MRT_ColumnDef<MinimalBrainForUser>[]>(
    () => [
      {
        accessorKey: "name",
        header: "name",
        size: 150,
      },
      {
        accessorKey: "description",
        header: "Description",
        size: 150,
      },
    ],
    []
  );

  const table = useMaterialReactTable({
    columns,
    data: brains,
  });

  return (
    <div className="flex flex-1 flex-col items-center justify-center">
      <div className="w-full lg:grid-cols-4 md:grid-cols-3 grid mt-5 gap-3 items-stretch">
        {brains.map((brain) => (
          <div key={brain.id} className="h-[180px]">
            <BrainItem brain={brain} />
          </div>
        ))}
      </div>
      <MaterialReactTable table={table} />
    </div>
  );
};
