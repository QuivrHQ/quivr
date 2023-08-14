import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";

interface QueryParams {
  value: string;
  focus: string;
  cf: string;
  fit: string;
  async: string;
  space: string;
  new: string;
  blur: string;
  combobox: string;
  mentions: string;
  enclosure: string;
}

export function useQueryParams() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const setQueryParam = useCallback(
    (name: keyof QueryParams, value = "true") => {
      const newSearchParams = new URLSearchParams(
        Object.fromEntries(searchParams)
      );
      newSearchParams.set(name, value);
      const search = newSearchParams.toString();
      const query = search ? `?${search}` : "";
      router.push(`${pathname}${query}`);
    },
    [pathname, router, searchParams]
  );

  const removeQueryParam = useCallback(
    (name: keyof QueryParams) => {
      const newSearchParams = new URLSearchParams(
        Object.fromEntries(searchParams)
      );
      newSearchParams.delete(name);
      const search = newSearchParams.toString();
      const query = search ? `?${search}` : "";
      router.push(`${pathname}${query}`);
    },
    [pathname, router, searchParams]
  );

  const updateQueryParam = useCallback(
    (name: keyof QueryParams, setParam: boolean) => {
      if (setParam) {
        setQueryParam(name);
      } else {
        removeQueryParam(name);
      }
    },
    [removeQueryParam, setQueryParam]
  );

  const hasQueryParams = useCallback(
    (name: keyof QueryParams) => searchParams.has(name),
    [searchParams]
  );

  const getQueryParam = useCallback(
    (name: keyof QueryParams) => searchParams.get(name),
    [searchParams]
  );

  return {
    setQueryParam,
    removeQueryParam,
    hasQueryParams,
    getQueryParam,
    updateQueryParam,
  };
}
