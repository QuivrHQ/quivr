# Changelog

## [0.0.16](https://github.com/QuivrHQ/quivr/compare/core-0.0.15...core-0.0.16) (2024-09-17)


### Bug Fixes

* **core:** enforce langchain &lt;0.3 for pydantic v1 ([#3217](https://github.com/QuivrHQ/quivr/issues/3217)) ([4bb4800](https://github.com/QuivrHQ/quivr/commit/4bb4800a76942ee31a939d3cacc94f057682177a))

## [0.0.15](https://github.com/QuivrHQ/quivr/compare/core-0.0.14...core-0.0.15) (2024-09-16)


### Features

* CRUD KMS (no syncs)  ([#3162](https://github.com/QuivrHQ/quivr/issues/3162)) ([71edca5](https://github.com/QuivrHQ/quivr/commit/71edca572ffd2901ed582005ac4b2803d9d95e57))
* save and load brain ([#3202](https://github.com/QuivrHQ/quivr/issues/3202)) ([eda619f](https://github.com/QuivrHQ/quivr/commit/eda619f4547921ab4c50458b2d44c6b5c10e40d1))


### Bug Fixes

* Update LLMEndpoint to include max_tokens parameter ([#3201](https://github.com/QuivrHQ/quivr/issues/3201)) ([13ed225](https://github.com/QuivrHQ/quivr/commit/13ed225b172407ee9826b9c01b2f7b124a8b5a10))

## [0.0.14](https://github.com/QuivrHQ/quivr/compare/core-0.0.13...core-0.0.14) (2024-09-09)


### Features

* Add brain_id and brain_name to ChatLLMMetadata model ([#2968](https://github.com/QuivrHQ/quivr/issues/2968)) ([1112001](https://github.com/QuivrHQ/quivr/commit/111200184b66dc42d75996c6c286474e9c5f8462))
* add chat with models ([#2933](https://github.com/QuivrHQ/quivr/issues/2933)) ([fccd197](https://github.com/QuivrHQ/quivr/commit/fccd197511d8594db257bfddf757bf0d28f7239d))
* Add get_model method to ModelRepository ([#2949](https://github.com/QuivrHQ/quivr/issues/2949)) ([13e9fc4](https://github.com/QuivrHQ/quivr/commit/13e9fc490bc62264de93d2efddf2389126c147fa))
* **anthropic:** add llm ([#3146](https://github.com/QuivrHQ/quivr/issues/3146)) ([8e29218](https://github.com/QuivrHQ/quivr/commit/8e2921886505cea0e72d2e1136a4b8ba862c3ce1))
* **azure:** quivr compatible with it ([#3005](https://github.com/QuivrHQ/quivr/issues/3005)) ([b5f31a8](https://github.com/QuivrHQ/quivr/commit/b5f31a83d4a1c4432943bbbaa0766c46927ef125))
* **frontend:** talk with models and handle code markdown ([#2980](https://github.com/QuivrHQ/quivr/issues/2980)) ([ef6037e](https://github.com/QuivrHQ/quivr/commit/ef6037e665f8d5e9c513d889773419a25f914d83))
* quivr core 0.1 ([#2970](https://github.com/QuivrHQ/quivr/issues/2970)) ([380cf82](https://github.com/QuivrHQ/quivr/commit/380cf8270678453c3dc14ac8665be9b3b5a49dce))
* using langgraph in our RAG pipeline ([#3130](https://github.com/QuivrHQ/quivr/issues/3130)) ([8cfdf53](https://github.com/QuivrHQ/quivr/commit/8cfdf53fe748b884cf44ade274503de3966b1378))


### Bug Fixes

* **chat:** order of chat history was reversed ([#3148](https://github.com/QuivrHQ/quivr/issues/3148)) ([7209500](https://github.com/QuivrHQ/quivr/commit/7209500d0bdaec544fce1e8e9082de3ead4464f4))

## [0.0.13](https://github.com/QuivrHQ/quivr/compare/core-0.0.12...core-0.0.13) (2024-08-01)


### Features

* quivr core tox test + parsers ([#2929](https://github.com/QuivrHQ/quivr/issues/2929)) ([6855585](https://github.com/QuivrHQ/quivr/commit/685558560cc431054fb9d1330c0e27ce5fdf1806))


### Bug Fixes

* processor quivr version ([#2934](https://github.com/QuivrHQ/quivr/issues/2934)) ([2d64962](https://github.com/QuivrHQ/quivr/commit/2d64962ca407d8f2c9e0faedc457548c3ff9921d))
* quivr core fix tests ([#2935](https://github.com/QuivrHQ/quivr/issues/2935)) ([d9c1f3a](https://github.com/QuivrHQ/quivr/commit/d9c1f3add48f354d92f3a21c03eca53add30a773))

## [0.0.12](https://github.com/QuivrHQ/quivr/compare/core-0.0.11...core-0.0.12) (2024-07-23)


### Features

* **dead-code:** removed composite & api ([#2902](https://github.com/QuivrHQ/quivr/issues/2902)) ([a2721d3](https://github.com/QuivrHQ/quivr/commit/a2721d3926df873e10817f948f8f10894ec6c581))
* **frontend:** add knowledge icon when integration ([#2888](https://github.com/QuivrHQ/quivr/issues/2888)) ([733d083](https://github.com/QuivrHQ/quivr/commit/733d083e330fc6e41c089bb9c9cf76289040cab9))

## [0.0.11](https://github.com/QuivrHQ/quivr/compare/core-0.0.10...core-0.0.11) (2024-07-22)


### Features

* move parsers quivr core ([#2884](https://github.com/QuivrHQ/quivr/issues/2884)) ([d3c53e6](https://github.com/QuivrHQ/quivr/commit/d3c53e63539bade5cbd716edf7e9af68ba15ed08))

## [0.0.10](https://github.com/QuivrHQ/quivr/compare/core-0.0.9...core-0.0.10) (2024-07-19)


### Features

* **frontend:** new notifications design ([#2870](https://github.com/QuivrHQ/quivr/issues/2870)) ([ed97004](https://github.com/QuivrHQ/quivr/commit/ed9700426959f3c1502a882263dfb447411d5381))
* **integrations:** dropbox ([#2864](https://github.com/QuivrHQ/quivr/issues/2864)) ([4806dc5](https://github.com/QuivrHQ/quivr/commit/4806dc5809aec9f7f573cb5adddac0e2d0ba600b))
* quivr core brain info + processors registry +  ([#2877](https://github.com/QuivrHQ/quivr/issues/2877)) ([3001fa1](https://github.com/QuivrHQ/quivr/commit/3001fa1475cf119a8b41a176f735f5402f708738))


### Bug Fixes

* Refacto & update dropbox refresh ([#2875](https://github.com/QuivrHQ/quivr/issues/2875)) ([3b68855](https://github.com/QuivrHQ/quivr/commit/3b68855a83c72f3e31c117af0434330383a8a5d7))

## [0.0.9](https://github.com/QuivrHQ/quivr/compare/core-0.0.8...core-0.0.9) (2024-07-15)


### Features

* quivr api use quivr core ([#2868](https://github.com/QuivrHQ/quivr/issues/2868)) ([9d3e9ed](https://github.com/QuivrHQ/quivr/commit/9d3e9edfd2ef24397458cc6556f6080673be96ae))


### Bug Fixes

* quiv core stream duplicate  and quivr-core rag tests ([#2852](https://github.com/QuivrHQ/quivr/issues/2852)) ([35eb07f](https://github.com/QuivrHQ/quivr/commit/35eb07f7a2664f65e482a78fabf242e1ccb36f07))

## [0.0.8](https://github.com/QuivrHQ/quivr/compare/core-0.0.7...core-0.0.8) (2024-07-11)


### Features

* Add Quivr chatbot example ([#2827](https://github.com/QuivrHQ/quivr/issues/2827)) ([5ff8d4e](https://github.com/QuivrHQ/quivr/commit/5ff8d4ee81cdc5a2cf375a6b7709beb44da2b911))
* Update aiofiles dependency to loosen version control ([#2834](https://github.com/QuivrHQ/quivr/issues/2834)) ([5e75d15](https://github.com/QuivrHQ/quivr/commit/5e75d155976dd710c65f9431e942cdeec9bd6424))

## [0.0.7](https://github.com/QuivrHQ/quivr/compare/core-0.0.6...core-0.0.7) (2024-07-10)


### Bug Fixes

* llm model name ([#2830](https://github.com/QuivrHQ/quivr/issues/2830)) ([71d6cd9](https://github.com/QuivrHQ/quivr/commit/71d6cd9b6b381226a172a09c07a0a084d7efbc22))

## [0.0.6](https://github.com/QuivrHQ/quivr/compare/core-0.0.5...core-0.0.6) (2024-07-10)


### Features

* quivr-core ask streaming ([#2828](https://github.com/QuivrHQ/quivr/issues/2828)) ([0658d49](https://github.com/QuivrHQ/quivr/commit/0658d4947c10f512d2ec2bdcfb70f089ab003a5c))

## [0.0.5](https://github.com/QuivrHQ/quivr/compare/core-0.0.4...core-0.0.5) (2024-07-10)


### Features

* Add GitHub Actions workflow for running tests on backend/core ([#2820](https://github.com/QuivrHQ/quivr/issues/2820)) ([82292f3](https://github.com/QuivrHQ/quivr/commit/82292f30acf982bbf28c1ef928440086fa342a04))
* Add GitHub Actions workflow for running tests on backend/core ([#2822](https://github.com/QuivrHQ/quivr/issues/2822)) ([1566040](https://github.com/QuivrHQ/quivr/commit/15660409a37af8df3c58a3f396614817c9f4641b))
* quivr core chat history ([#2824](https://github.com/QuivrHQ/quivr/issues/2824)) ([847e161](https://github.com/QuivrHQ/quivr/commit/847e161d804421e60eb246f35bf51b7ffd88f3a2))

## [0.0.4](https://github.com/QuivrHQ/quivr/compare/core-0.0.3...core-0.0.4) (2024-07-09)


### Features

* quivr core minimal chat ([#2818](https://github.com/QuivrHQ/quivr/issues/2818)) ([481f24f](https://github.com/QuivrHQ/quivr/commit/481f24f5bed855d044c97eb881512fbf936772f8))

## [0.0.3](https://github.com/QuivrHQ/quivr/compare/core-0.0.2...core-0.0.3) (2024-07-09)


### Bug Fixes

* **pyproject:** fixed to quivr github ([#2816](https://github.com/QuivrHQ/quivr/issues/2816)) ([5a4ac00](https://github.com/QuivrHQ/quivr/commit/5a4ac001d0ba26af0c48aea7d9807c66b5fdd48d))

## [0.0.2](https://github.com/QuivrHQ/quivr/compare/core-v0.0.1...core-0.0.2) (2024-07-09)


### Features

* **backend:** quivr-monorepo and quivr-core package ([#2765](https://github.com/QuivrHQ/quivr/issues/2765)) ([2e75de4](https://github.com/QuivrHQ/quivr/commit/2e75de40390bcc09f25037f19693989841fec70d))
* quivr core minimal chat ([#2803](https://github.com/QuivrHQ/quivr/issues/2803)) ([1dc6d88](https://github.com/QuivrHQ/quivr/commit/1dc6d88f9b8b1b0c1a5682f990bf8098cbd54d77))
