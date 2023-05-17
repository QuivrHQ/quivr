import Image from 'next/image'
import styles from './page.module.css'

export default function Home() {
  return (
    <main className={styles.main}>
      <div className={styles.description}>
        <p>
          Welcome to Quivr, your second brain with GenerativeAI 🧠
        </p>
      </div>
      <div className={styles.center}>
        <iframe
          src="https://github.com/StanGirard/quivr/assets/19614572/80721777-2313-468f-b75e-09379f694653"
          width="720"
          height="480"
          frameborder="0"
          allow="autoplay; fullscreen; picture-in-picture"
          allowFullScreen
        ></iframe>
      </div>
      <p>Stay up to date 👇</p>
      <iframe
        src="https://embeds.beehiiv.com/a75f7917-1d4b-4c3c-8d4a-b6891d6e19e3?slim=true"
        data-test-id="beehiiv-embed"
        height="52"
        style = {{width: "100%", maxWidth: "500px", margin: "0 auto", display: "block"}}
      ></iframe>

      <div className={styles.grid}>
        <a
          href="https://github.com/StanGirard/quivr"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            GitHub <span>-&gt;</span>
          </h2>
          <p>Check out the source code on GitHub.</p>
        </a>

        <a
          href="https://twitter.com/_StanGirard"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Twitter <span>-&gt;</span>
          </h2>
          <p>Follow us on Twitter for updates.</p>
        </a>

        <a
          href="https://discord.gg/HUpRgp2HG8"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Discord <span>-&gt;</span>
          </h2>
          <p>Join the discussion on Discord</p>
        </a>

        <a
          href="https://try-quivr.streamlit.app"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Demo <span>-&gt;</span>
          </h2>
          <p>Try our live demo</p>
        </a>

      </div>
    </main>
  )
}