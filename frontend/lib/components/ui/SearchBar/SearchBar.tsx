import { ChangeEvent, Dispatch, SetStateAction, useState } from 'react';
import { LuSearch } from "react-icons/lu";

import styles from './SearchBar.module.scss'
import { useChatInput } from '@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput';

export const SearchBar = (): JSX.Element => {
    const { message, setMessage, submitQuestion } = useChatInput();

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        setMessage(event.target.value);
    };

    const handleEnter = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            submit()
        }
    };

    const submit = () => {
        submitQuestion();
    }

    /* eslint-disable @typescript-eslint/restrict-template-expressions */

    return (
        <div className={styles.search_bar_wrapper}>
            <input
                className={styles.search_input}
                type="text"
                placeholder="Search"
                value={message}
                onChange={handleChange}
                onKeyDown={handleEnter}
            />
            <LuSearch
                className={`${styles.search_icon} ${!message ? styles.disabled : ''}`}
                onClick={submit}
            />
        </div>
    )
}