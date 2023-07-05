# Quivr - Your Second Brain, Empowered by Generative AI

<div align="center">
    <img src="./logo.png" alt="Quivr-logo" width="30%"  style="border-radius: 50%; padding-bottom: 20px"/>
</div>

<div align="center">
<a href="https://discord.gg/HUpRgp2HG8">
  <img src="https://img.shields.io/badge/discord-join%20chat-blue.svg" alt="Join our Discord" height="40">
</a>
</div>

Quivr, your second brain, utilizes the power of GenerativeAI to store and retrieve unstructured information. Think of it as Obsidian, but turbocharged with AI capabilities.

[Roadmap here](https://brain.quivr.app)

## Key Features 🎯

- **Universal Data Acceptance**: Quivr can handle almost any type of data you throw at it. Text, images, code snippets, we've got you covered.
- **Generative AI**: Quivr employs advanced AI to assist you in generating and retrieving information.
- **Fast and Efficient**: Designed with speed and efficiency at its core. Quivr ensures rapid access to your data.
- **Secure**: Your data, your control. Always.
- **OS Compatible**: Ubuntu 22 or upper.
- **File Compatibility**: 
  - Text
  - Markdown
  - PDF
  - Powerpoint
  - Excel (Not Yet)
  - Csv
  - Word
  - Audio
  - Video
- **Open Source**: Freedom is beautiful, so is Quivr. Open source and free to use.

## Demo Highlights 🎥

https://github.com/StanGirard/quivr/assets/19614572/a6463b73-76c7-4bc0-978d-70562dca71f5

## Getting Started: 🚀

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

You can find everything on the documentation [here](https://brain.quivr.app/)

### Prerequisites 📋

Before you proceed, ensure you have the following installed:

- Docker
- Docker Compose

Additionally, you'll need a [Supabase](https://supabase.com/) account for:

- Creating a new Supabase project
- Supabase Project API key
- Supabase Project URL

### Installation Steps 💽

- **Step 0**: If needed, here is the installation explained on Youtube [here](https://youtu.be/rC-s4QdfY80)

- **Step 1**: Clone the repository using **one** of these commands:

  - If you don't have an SSH key set up:
  
  ```bash
  git clone https://github.com/StanGirard/Quivr.git && cd Quivr
  ```
  - If you have an SSH key set up or want to add it ([guide here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account))
  
  ```bash
  git clone git@github.com:StanGirard/Quivr.git && cd Quivr
  ```

- ** Step 2**: Use the install helper

You can use the install_helper.sh script to setup your env files

```bash
brew install gum # Windows (via Scoop) scoop install charm-gum

chmod +x install_helper.sh
./install_helper.sh
```

- **Step 2 - Bis**: Copy the `.XXXXX_env` files

```bash
cp .backend_env.example backend/.env
cp .frontend_env.example frontend/.env
```

- **Step 3**: Update the `backend/.env` and `frontend/.env` file 

> _Your `supabase_service_key` can be found in your Supabase dashboard under Project Settings -> API. Use the `anon` `public` key found in the `Project API keys` section._


> _Your  `JWT_SECRET_KEY`can be found in your supabase settings under Project Settings -> API -> JWT Settings -> JWT Secret_

> _To activate vertexAI with PaLM from GCP follow the instructions [here](https://python.langchain.com/en/latest/modules/models/llms/integrations/google_vertex_ai_palm.html) and update `backend/.env`- It is an advanced feature, please be expert in GCP before trying to use it_

- [ ] Change variables in `backend/.env`
- [ ] Change variables in `frontend/.env`

- **Step 4**: Run the following migration scripts on the Supabase database via the web interface (SQL Editor -> `New query`)

Use the `migration.sh` script to run the migration scripts

```bash
chmod +x migration.sh
./migration.sh
```

And choose either create_scripts if first time or migrations if you are updating your database


All scripts can be found in the [scripts](scripts/) folder
> _If you come from an old version of Quivr, run the scripts in [migration script](scripts/) to migrate your data to the new version in the order of date_

- **Step 5**: Launch the app

```bash
docker compose -f docker-compose.yml up --build
```

- **Step 6**: Navigate to `localhost:3000` in your browser

- ** Step 7**: Want to contribute to the project? 

```
docker compose -f docker-compose.dev.yml up --build
```



## Contributors ✨

Thanks goes to these wonderful people:
<a href="https://github.com/stangirard/quivr/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=stangirard/quivr" />
</a>

## Contribute 🤝

Got a pull request? Open it, and we'll review it as soon as possible. Check out our project board [here](https://github.com/users/StanGirard/projects/5) to see what we're currently focused on, and feel free to bring your fresh ideas to the table!


- [Open Issues](https://github.com/StanGirard/quivr/issues)
- [Open Pull Requests](https://github.com/StanGirard/quivr/pulls)
- [Good First Issues](https://github.com/StanGirard/quivr/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)
- [Frontend Issues](https://github.com/StanGirard/quivr/issues?q=is%3Aopen+is%3Aissue+label%3Afrontend)
- [Backend Issues](https://github.com/StanGirard/quivr/issues?q=is%3Aopen+is%3Aissue+label%3Abackend)

## Sponsors ❤️

This project could not be possible without the support of our sponsors. Thank you for your support!

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



## License 📄

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details


## Stars History 📈

[![Star History Chart](https://api.star-history.com/svg?repos=StanGirard/quivr&type=Timeline)](https://star-history.com/#StanGirard/quivr&Timeline)
