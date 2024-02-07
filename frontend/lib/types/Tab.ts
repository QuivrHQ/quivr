export interface Tab {
  label: string;
  isSelected: boolean;
  disabled?: boolean;
  onClick: () => void;
}
