"use client";
import { BeautifulMentionsMenuProps } from "lexical-beautiful-mentions";
import { forwardRef } from "react";

export const Menu = forwardRef<any, BeautifulMentionsMenuProps>(
  ({ open, loading, ...other }, ref) => {
    if (loading) {
      return (
        <div
          ref={ref}
          className="mt-6 whitespace-nowrap rounded-lg bg-white p-2.5 text-slate-950 shadow-lg shadow-gray-900 dark:bg-gray-900 dark:text-slate-300"
        >
          Loading...
        </div>
      );
    }

    return (
      <ul
        ref={ref}
        style={{
          scrollbarWidth: "none",
          msOverflowStyle: "none",
        }}
        className="m-0 mt-6 list-none overflow-scroll overflow-y-scroll rounded-lg bg-white p-0 shadow-lg shadow-gray-900 dark:bg-gray-900"
        {...other}
      />
    );
  }
);
