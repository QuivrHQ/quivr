import {
  Language,
  useLanguageHook,
} from "@/app/user/components/LanguageSelect/hooks/useLanguageHook";

import styles from "./CountrySelector.module.scss";

import { FieldHeader } from "../FieldHeader/FieldHeader";

type CountrySelectorProps = {
  iconName: string;
  label: string;
  currentValue: { label: string; flag: string };
  setCurrentValue: (newCountry: Language) => void;
};

export const CountrySelector = ({
  iconName,
  label,
  currentValue,
  setCurrentValue,
}: CountrySelectorProps): JSX.Element => {
  const { allLanguages } = useLanguageHook();

  return (
    <div className={styles.country_selector_container}>
      <FieldHeader iconName={iconName} label={label} />
      <select
        className={styles.selection}
        data-testid="language-select"
        name="language"
        id="language"
        value={currentValue.label}
        onChange={(e) =>
          setCurrentValue(
            allLanguages.find(
              (language) => language.label === e.target.value
            ) ?? allLanguages[2]
          )
        }
      >
        {allLanguages.map((lang) => (
          <option
            data-testid={`option-${lang}`}
            value={lang.label}
            key={lang.shortName}
          >
            {lang.flag} {lang.label}
          </option>
        ))}
      </select>
    </div>
  );
};
