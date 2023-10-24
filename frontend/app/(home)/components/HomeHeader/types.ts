export type NavbarItem = {
  href: string;
  label: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode | null;
  newTab?: boolean;
  className?: string;
};
