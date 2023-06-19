const Footer = (): JSX.Element => {
  return (
    <footer className="bg-white dark:bg-black border-t dark:border-white/10 mt-auto py-10">
      <div className="max-w-screen-xl mx-auto flex justify-center items-center gap-4">
        <a
          href="https://github.com/stangirard/quivr"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Quivr GitHub"
        >
          <img
            className="h-8 w-auto dark:invert"
            src="/github.svg"
            alt="GitHub"
          />
        </a>
        <a
          href="https://twitter.com/quivr_brain"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Quivr Twitter"
        >
          <img className="h-8 w-auto" src="/twitter.svg" alt="Twitter" />
        </a>
      </div>
    </footer>
  );
};

export default Footer;
