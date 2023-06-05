
const Footer = () => {
  return (
    <footer className="bg-white dark:bg-black border-t dark:border-white/10 py-4 mt-auto">
      <div className="max-w-screen-xl mx-auto flex justify-center items-center gap-4">
        <a
          href="https://github.com/stangirard/quivr"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Quivr GitHub"
        >
          <img
            className="h-8 w-auto"
            src="/github.svg"
            alt="GitHub"
          />
        </a>
        <a
          href="https://twitter.com/Quivr_app"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Quivr Twitter"
        >
          <img
            className="h-8 w-auto"
            src="/twitter.svg"
            alt="Twitter"
          />
        </a>
      </div>
    </footer>
  );
};

export default Footer;