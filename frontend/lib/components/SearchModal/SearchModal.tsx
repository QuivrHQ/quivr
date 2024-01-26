import { useEffect, useRef, useState } from "react";

import styles from "./SearchModal.module.scss";

import { SearchBar } from "../ui/SearchBar/SearchBar";

export const SearchModal = (): JSX.Element => {
  const [isVisible, setIsVisible] = useState(false);
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

  const mousedownHandler = (event: MouseEvent) => {
    if (
      !(searchBarRef.current as HTMLElement | null)?.contains(
        event.target as Node
      )
    ) {
      setIsVisible(false);
    }
  };

  useEffect(() => {
    document.addEventListener("keydown", keydownHandler);
    window.addEventListener("click", mousedownHandler);

    return () => {
      document.removeEventListener("keydown", keydownHandler);
      window.removeEventListener("click", mousedownHandler);
    };
  }, []);

  if (!isVisible) {
    return <></>;
  }

  return (
    <div className={styles.search_modal_wrapper}>
      <div className={styles.search_bar_wrapper} ref={searchBarRef}>
        <SearchBar />
      </div>
    </div>
  );
};

export default SearchModal;
