import { UUID } from "crypto";

export type SelectOptionProps<T> = {
  label: string;
  value: T;
};

type SelectProps<T> = {
  options: SelectOptionProps<T>[];
  onChange: (option: T) => void;
  selectedOption: SelectOptionProps<T> | undefined;
};

export const SingleSelector = <T extends string | number | UUID>({
  onChange,
  options,
  selectedOption,
}: SelectProps<T>): JSX.Element => {
  console.info(onChange, options, selectedOption);

  return <div></div>;
};
