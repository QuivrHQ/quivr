import { ChangeEvent } from 'react';
import { LuSearch } from "react-icons/lu";

import { useChatInput } from '@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput';
import { useChat } from '@/app/chat/[chatId]/hooks/useChat';
import { useChatContext } from '@/lib/context';

import styles from './SearchBar.module.scss';

export const SearchBar = (): JSX.Element => {
    const { message, setMessage } = useChatInput()
    const { setMessages } = useChatContext()
    const { addQuestion } = useChat()

    const handleChange = (event: ChangeEvent<HTMLInputElement>): void => {
        setMessage(event.target.value);
    };

    const handleEnter = async (event: React.KeyboardEvent<HTMLInputElement>): Promise<void> => {
        if (event.key === 'Enter') {
            await submit()
        }
    };

    const submit = async (): Promise<void> => {
        setMessages([]);
        try {
            await addQuestion(message);
        } catch (error) {
            console.error(error);
        }
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
                onKeyDown={(event) => void handleEnter(event)}
            />
            <LuSearch
                className={`${styles.search_icon} ${!message ? styles.disabled : ''}`}
                onClick={() => void submit()}
            />
        </div>
    )
}