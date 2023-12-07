# Quivr - Your Second Brain, Empowered by Generative AI

<div align="center">
    <img src="./logo.png" alt="Quivr-logo" width="30%"  style="border-radius: 50%; padding-bottom: 20px"/>
</div>

[![Discord Follow](https://dcbadge.vercel.app/api/server/HUpRgp2HG8?style=flat)](https://discord.gg/HUpRgp2HG8)
[![GitHub Repo stars](https://img.shields.io/github/stars/stangirard/quivr?style=social)](https://github.com/stangirard/quivr)
[![Twitter Follow](https://img.shields.io/twitter/follow/StanGirard?style=social)](https://twitter.com/_StanGirard)

Quivr, your second brain, utilizes the power of GenerativeAI to be your personal assistant ! Think of it as Obsidian, but turbocharged with AI capabilities.

[Roadmap here](https://brain.quivr.app/docs/roadmap)

## Key Features 🎯

- **Fast and Efficient**: Designed with speed and efficiency at its core. Quivr ensures rapid access to your data.
- **Secure**: Your data, your control. Always.
- **OS Compatible**: Ubuntu 22 or newer.
- **File Compatibility**: Text, Markdown, PDF, Powerpoint, Excel, CSV, Word, Audio, Video
- **Open Source**: Freedom is beautiful, and so is Quivr. Open source and free to use.
- **Public/Private**: Share your brains with your users via a public link, or keep them private.
- **Marketplace**: Share your brains with the world, or use other people's brains to boost your productivity.
- **Offline Mode**: Quivr works offline, so you can access your data anytime, anywhere.

## Demo Highlights 🎥

https://github.com/StanGirard/quivr/assets/19614572/a6463b73-76c7-4bc0-978d-70562dca71f5

## Getting Started 🚀

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

You can find everything on the [documentation](https://brain.quivr.app/).

### Prerequisites 📋

Ensure you have the following installed:

- Docker
- Docker Compose

### 60 seconds Installation 💽

You can find the installation video [here](https://www.youtube.com/watch?v=cXBa6dZJN48).

- **Step 1**: Clone the repository:

  ```bash
  git clone https://github.com/StanGirard/Quivr.git && cd Quivr
  ```

- **Step 2**: Copy the `.env.example` files

  ```bash
  cp .env.example .env
  ```

- **Step 3**: Update the `.env` files

  ```bash
  vim .env # or emacs or vscode or nano
  ```

  Update **OPENAI_API_KEY** in the `.env` file.

  You just need to update the `OPENAI_API_KEY` variable in the `.env` file. You can get your API key [here](https://platform.openai.com/api-keys). You need to create an account first. And put your credit card information. Don't worry, you won't be charged unless you use the API. You can find more information about the pricing [here](https://openai.com/pricing/).

  > Want to use [Ollama.ai](https://ollama.ai) instead?
  > Uncomment the following lines in the `.env` file:
  > OLLAMA_API_BASE_URL
  > Run the following command to start Ollama: `ollama run llama2`
  > You can find more information about Ollama [here](https://ollama.ai/).

- **Step 4**: Launch the project

  ```bash
  docker compose pull
  docker compose up --build # if OPENAI
  # docker compose -f docker-compose-ollama.yml up --build  # Only if using Ollama. You need to run `ollama run llama2` first.
  ```

  If you have a Mac, go to Docker Desktop > Settings > General and check that the "file sharing implementation" is set to `VirtioFS`.

  If you are a developer, you can run the project in development mode with the following command: `docker compose -f docker-compose.dev.yml up --build`

- **Step 5**: Login to the app

  Connect to the supabase database at [http://localhost:8000/project/default/auth/users](http://localhost:8000/project/default/auth/users) with the following credentials: admin/admin in order to create new users. Auto-confirm the email.

  You can now sign in to the app with your new user. You can access the app at [http://localhost:3000/login](http://localhost:3000/login).

  You can access Quivr backend API at [http://localhost:5050/docs](http://localhost:5050/docs)

## Updating Quivr 🚀

- **Step 1**: Pull the latest changes

  ```bash
  git pull
  ```

- **Step 2**: Use the `migration.sh` script to run the migration scripts

  ```bash
  chmod +x migration.sh # You need to install Gum & postgresql (brew install gum for example)
  ./migration.sh
  # Select  2) Run migrations
  ```

  Alternatively, you can run the script on the Supabase database via the web
  interface (SQL Editor -> `New query` -> paste the script -> `Run`)

  All the scripts can be found in the [scripts](scripts/) folder

## Contributors ✨

Thanks go to these wonderful people:
<a href="https://github.com/stangirard/quivr/graphs/contributors">
<img src="https://contrib.rocks/image?repo=stangirard/quivr" />
</a>

## Contribute 🤝

Did you get a pull request? Open it, and we'll review it as soon as possible. Check out our project board [here](https://github.com/users/StanGirard/projects/5) to see what we're currently focused on, and feel free to bring your fresh ideas to the table!

- [Open Issues](https://github.com/StanGirard/quivr/issues)
- [Open Pull Requests](https://github.com/StanGirard/quivr/pulls)
- [Good First Issues](https://github.com/StanGirard/quivr/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)
- [Frontend Issues](https://github.com/StanGirard/quivr/issues?q=is%3Aopen+is%3Aissue+label%3Afrontend)
- [Backend Issues](https://github.com/StanGirard/quivr/issues?q=is%3Aopen+is%3Aissue+label%3Abackend)

## Sponsors ❤️

This project would not be possible without the support of our sponsors. Thank you for your support!

<a href="https://www.theodo.fr/">
  <img src="https://avatars.githubusercontent.com/u/332041?s=200&v=4" alt="Theodo" style="padding: 10px" width="70px">
</a>
<a href="https://www.padok.fr/">
  <img src="https://avatars.githubusercontent.com/u/46325765?s=200&v=4" alt="Padok" style="padding: 10px" width="70px">
</a>
<a href="https://www.aleios.com/">
  <img src="https://avatars.githubusercontent.com/u/97908131?s=200&v=4" alt="Aleios" style="padding: 10px" width="70px">
</a>
<a href="https://www.bam.tech/">
  <img src="https://avatars.githubusercontent.com/u/9597329?s=200&v=4" alt="BAM" style="padding: 10px" width="70px">
</a>
<a href="https://www.sicara.fr/">
  <img src="https://avatars.githubusercontent.com/u/23194788?s=200&v=4" alt="Sicara" style="padding: 10px" width="70px">
</a>

## License 📄

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details

## Stars History 📈

[![Star History Chart](https://api.star-history.com/svg?repos=StanGirard/quivr&type=Timeline)](https://star-history.com/#StanGirard/quivr&Timeline)
