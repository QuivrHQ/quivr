// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion



/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Quivr 🧠',
  tagline: 'Your Generative AI second brain',
  favicon: 'img/quivr-logo.ico',

  // Set the production url of your site here
  url: 'https://brain.quivr.app',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'stangirard', // Usually your GitHub org/user name.
  projectName: 'quivr', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/StanGirard/quivr/tree/main/docs/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/StanGirard/quivr/tree/main/docs/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/logo.png',
      navbar: {
        title: 'Quivr',
        logo: {
          alt: 'Quivr logo',
          src: 'img/logo.png',
        },
        items: [
          {
            href: 'https://quivr.app',
            position: 'right',
            label: 'Try me now',
          },
          {
            href: 'https://github.com/stangirard/Quivr',
            label: 'Star us on GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Get Started',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Discord',
                href: 'http://discord.gg/HUpRgp2HG8',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/quivr_brain',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Website',
                to: 'https://quivr.app',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/stangirard/Quivr',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Quivr`,
      },
      algolia: {
        // The application ID provided by Algolia
        appId: '4CC1BF1YRT',
  
        // Public API key: it is safe to commit it
        apiKey: '20034381e8836ebc0eedf3f8b251b0eb',
  
        indexName: 'brain',
  
        // Optional: see doc section below
        contextualSearch: true,
  
  
        // Optional: Algolia search parameters
        searchParameters: {},
  
        // Optional: path for search page that enabled by default (`false` to disable it)
        searchPagePath: 'search',
  
        //... other Algolia params
      },
  
    }),
};

module.exports = config;
