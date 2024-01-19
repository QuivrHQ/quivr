import { ChangeEvent, Dispatch, SetStateAction, useState } from 'react';
import { LuSearch } from "react-icons/lu";

import styles from './SearchBar.module.scss'

export const SearchBar = (): JSX.Element => {
    const [inputValue, setInputValue]: [string, Dispatch<SetStateAction<string>>] = useState<string>('');

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        setInputValue(event.target.value);
    };

    const handleEnter = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            submit()
        }
    };

    const submit = () => {
        console.info('submit')
    }

    /* eslint-disable @typescript-eslint/restrict-template-expressions */

    return (
        <div className={styles.search_bar_wrapper}>
            <input
                className={styles.search_input}
                type="text"
                placeholder="Search"
                value={inputValue}
                onChange={handleChange}
                onKeyDown={handleEnter}
            />
            <LuSearch
                className={`${styles.search_icon} ${!inputValue ? styles.disabled : ''}`}
                onClick={submit} />
        </div>
    )
}