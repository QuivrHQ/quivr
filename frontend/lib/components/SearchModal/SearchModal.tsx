import { useEffect, useRef } from "react";

import { useSearchModalContext } from "@/lib/context/SearchModalProvider/hooks/useSearchModalContext";

import styles from "./SearchModal.module.scss";

import { SearchBar } from "../ui/SearchBar/SearchBar";

export const SearchModal = (): JSX.Element => {
  const { isVisible, setIsVisible } = useSearchModalContext();
  const searchBarRef = useRef(null);

  const keydownHandler = ({
    key,
    metaKey,
  }: {
    key: string;
    metaKey: boolean;
  }) => {
    if (metaKey && key === "k") {
      setIsVisible(true);
    } else if (key === "Escape") {
      setIsVisible(false);
    }
  };

  const clickHandler = (event: MouseEvent) => {
    if (
      !(searchBarRef.current as HTMLElement | null)?.contains(
        event.target as Node
      )
    ) {
      setIsVisible(false);
    }
  };

  const handleSearch = () => {
    setIsVisible(false);
  };

  useEffect(() => {
    window.addEventListener("keydown", keydownHandler);
    window.addEventListener("click", clickHandler);

    return () => {
      window.removeEventListener("keydown", keydownHandler);
      window.removeEventListener("click", clickHandler);
    };
  }, []);

  if (!isVisible) {
    return <></>;
  }

  return (
    <div className={styles.search_modal_wrapper}>
      <div className={styles.search_bar_wrapper} ref={searchBarRef}>
        <SearchBar onSearch={handleSearch} />
      </div>
    </div>
  );
};

export default SearchModal;
