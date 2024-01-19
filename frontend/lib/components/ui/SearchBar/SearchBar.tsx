import styles from './SearchBar.module.scss'

export const SearchBar = (): JSX.Element => {
    return (
        <div className={styles.search_bar_wrapper}>
            <input
                className={styles.search_input}
                type="text"
                placeholder="Search"
            />
        </div>
    )
}