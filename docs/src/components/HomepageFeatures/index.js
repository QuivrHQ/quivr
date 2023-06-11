import clsx from 'clsx';
import React from 'react';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Universal Data Acceptance',
    description: (
      <>
        Quivr can handle almost any type of data you throw at it. Text, images,
        code snippets, we've got you covered.
      </>
    ),
  },
  {
    title: 'Generative AI',
    description: (
      <>
        Quivr employs advanced AI to assist you in generating and retrieving information.
      </>
    ),
  },
  {
    title: 'Fast and Efficient',
    description: (
      <>
        Designed with speed and efficiency at its core. Quivr ensures rapid access to your data.
      </>
    ),
  },
  {
    title: 'Secure',
    description: (
      <>
        Your data, your control. Always.
      </>
    ),
  },
  {
    title: 'File Compatibility',
    description: (
      <>
        Quivr is compatible with Text, Markdown, PDF, Powerpoint, Excel, Word, Audio, and Video files.
      </>
    ),
  },
  {
    title: 'Open Source',
    description: (
      <>
        Freedom is beautiful, so is Quivr. Open source and free to use.
      </>
    ),
  },
];

function Feature({ title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
