/* eslint-disable */
import { useState } from "react";

import { NavItems } from "./NavItems";

export const MobileMenu = (): JSX.Element => {
  const [open, setOpen] = useState(false); 

  return (
    <div className="md:hidden flex flex-row items-center justify-between  px-6 sm:hidden">
        <NavItems
            setOpen={setOpen}
            className="text-3xl gap-10"
        />
    </div>
);
};
