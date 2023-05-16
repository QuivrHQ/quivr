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
          src="https://github.com/StanGirard/Quivr/assets/19614572/a3cddc6a-ca28-44ad-9ede-3122fa918b51" 
          width="1000" 
          height="480" 
          frameborder="0" 
          allow="autoplay; fullscreen; picture-in-picture" 
          allowFullScreen
        ></iframe>
      </div>
      <div className={styles.grid}>
  <a
    href="https://github.com/StanGirard"
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


</div>
    </main>
  )
}