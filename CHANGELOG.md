# Changelog

## [0.0.61](https://github.com/StanGirard/quivr/compare/v0.0.60...v0.0.61) (2023-08-23)


### Features

* add brain prompt overwritting from chat ([#1012](https://github.com/StanGirard/quivr/issues/1012)) ([b967c2d](https://github.com/StanGirard/quivr/commit/b967c2d2d60b93f9142fe2afd04fb9422adcc2be))
* **backend:** adds python code parsing ([#1003](https://github.com/StanGirard/quivr/issues/1003)) ([a626b84](https://github.com/StanGirard/quivr/commit/a626b84b96c7b40904960e039f72ff042148a240))
* **prompts:** add public prompts to SQL db ([#1014](https://github.com/StanGirard/quivr/issues/1014)) ([4b1f4b1](https://github.com/StanGirard/quivr/commit/4b1f4b141287d109794aa6015f83deb3882ac5cb))
* **translation:** Added Simplified Chinese translation，Fix pt-br not working ([#1011](https://github.com/StanGirard/quivr/issues/1011)) ([e328ab8](https://github.com/StanGirard/quivr/commit/e328ab81b30f2dd3dae7287e0351fdacd1c18133))


### Bug Fixes

* **Analytics:** no tags tracking for upload & crawl ([#1024](https://github.com/StanGirard/quivr/issues/1024)) ([2b74ebc](https://github.com/StanGirard/quivr/commit/2b74ebc1f099c4d12705d458fefad94120af9208))

## [0.0.60](https://github.com/StanGirard/quivr/compare/v0.0.59...v0.0.60) (2023-08-22)


### Features

* **chat:** add brain selection through mention input ([#969](https://github.com/StanGirard/quivr/issues/969)) ([8e94f22](https://github.com/StanGirard/quivr/commit/8e94f22782dd2255e8125fbb4b3718413ad4701e))


### Bug Fixes

* remove conflicts ([#998](https://github.com/StanGirard/quivr/issues/998)) ([f61b70a](https://github.com/StanGirard/quivr/commit/f61b70a34f6d24e6f343d31cc4aa63265bb1c218))
* update backend tests ([#992](https://github.com/StanGirard/quivr/issues/992)) ([5a3a6fe](https://github.com/StanGirard/quivr/commit/5a3a6fe370756783a204f2a62007f6cb23c7b202))

## [0.0.59](https://github.com/StanGirard/quivr/compare/v0.0.58...v0.0.59) (2023-08-20)


### Features

* **aws:** all in microservices ([b3a6231](https://github.com/StanGirard/quivr/commit/b3a6231274e5aea28675381ba6f7ba277228f5ac))
* **chat-service:** added task definition ([d001ec7](https://github.com/StanGirard/quivr/commit/d001ec70df3ccd5f3885b5f174e58f1b3238c433))
* **docker:** improved size image ([#978](https://github.com/StanGirard/quivr/issues/978)) ([aa623c4](https://github.com/StanGirard/quivr/commit/aa623c4039ba31928dd0934a682259c7762d2efa))
* **docker:** pushing image to github registry ([ad3dca3](https://github.com/StanGirard/quivr/commit/ad3dca3e2705b87a9c9c0b35f67773bcc182ae88))
* **gcr:** removed sha and put latest ([2b85a94](https://github.com/StanGirard/quivr/commit/2b85a94e8835861afd9c178b72e59d018d8b956f))
* **health:** added endpoint for services ([#989](https://github.com/StanGirard/quivr/issues/989)) ([ae7852e](https://github.com/StanGirard/quivr/commit/ae7852ec3f9d6e20b28c3b6fbc0d433d476395ea))
* **microservices:** split into 4 quivr to better handle long services ([#972](https://github.com/StanGirard/quivr/issues/972)) ([7281fd9](https://github.com/StanGirard/quivr/commit/7281fd905a24b8e4dad7214d7809b8856685fca8))
* **preview:** added crawl service to ci ([b7f9876](https://github.com/StanGirard/quivr/commit/b7f9876ce20a2c802ccfd7cff35de50ac2fd2226))
* **preview:** added preview ([#974](https://github.com/StanGirard/quivr/issues/974)) ([9eb25a4](https://github.com/StanGirard/quivr/commit/9eb25a4d1777b9fdbc1c4b93df0b51e8b28d3ae9))
* **preview:** added service upload ([#979](https://github.com/StanGirard/quivr/issues/979)) ([ce6b45e](https://github.com/StanGirard/quivr/commit/ce6b45e1ac8e9a3d21b7f56ad228351e34179e11))
* **refacto:** changed a bit of things to make better dx ([#984](https://github.com/StanGirard/quivr/issues/984)) ([d0370ab](https://github.com/StanGirard/quivr/commit/d0370ab499465ee1404d3c1d32878e8da3853441))
* **Unplug:** chatting without brain streaming ([#970](https://github.com/StanGirard/quivr/issues/970)) ([600ff1e](https://github.com/StanGirard/quivr/commit/600ff1ede02741c66853cc3e4e7f5001aaba3bc2))


### Bug Fixes

* **settings:** select proper brain model ([#943](https://github.com/StanGirard/quivr/issues/943)) ([3a44f54](https://github.com/StanGirard/quivr/commit/3a44f54d6b75581e3cbc8acf0c1c309c3273e63f))
* update backend tests ([#975](https://github.com/StanGirard/quivr/issues/975)) ([c746eb1](https://github.com/StanGirard/quivr/commit/c746eb18303945a1736c89427026b509f501e715))
* **windows:** removed unused start script ([#962](https://github.com/StanGirard/quivr/issues/962)) ([ad7ac15](https://github.com/StanGirard/quivr/commit/ad7ac1516d5c45c833c9e9ba6162012096372fa6))

## [0.0.57](https://github.com/StanGirard/quivr/compare/v0.0.56...v0.0.57) (2023-08-16)


### Features

* add brain missing message ([#958](https://github.com/StanGirard/quivr/issues/958)) ([f99f81d](https://github.com/StanGirard/quivr/commit/f99f81d10f9c768af00e38249763a252f8db16e3))
* change messages position ([#946](https://github.com/StanGirard/quivr/issues/946)) ([9235a84](https://github.com/StanGirard/quivr/commit/9235a848d12b96af346cc2cbb1ac50dc2f67b20c))
* update chat ui ([#907](https://github.com/StanGirard/quivr/issues/907)) ([80be40a](https://github.com/StanGirard/quivr/commit/80be40ad34d07b646d48d2aa0405a92b3de308d7))


### Bug Fixes

* **chat routes:** use brain model, temp, and token ([#902](https://github.com/StanGirard/quivr/issues/902)) ([59ddfb4](https://github.com/StanGirard/quivr/commit/59ddfb48823b56239fe7fc95133274a3bedf49da))
* **chatMessages:** Fix error on answering question ([#953](https://github.com/StanGirard/quivr/issues/953)) ([1fef9b0](https://github.com/StanGirard/quivr/commit/1fef9b078379c8991f6029c34ac10d4cbdc5a44d))
* **crawler:** using newspaper and fixed recursive by merging content ([#955](https://github.com/StanGirard/quivr/issues/955)) ([d7c5c79](https://github.com/StanGirard/quivr/commit/d7c5c79043827b2b0949f6fd6c508c4617dcf498))
* **translations:** pr portuguese translations ([#933](https://github.com/StanGirard/quivr/issues/933)) ([d80178a](https://github.com/StanGirard/quivr/commit/d80178a84802c35b2c13d3eef4d0438fd067da92))

## [0.0.56](https://github.com/StanGirard/quivr/compare/v0.0.55...v0.0.56) (2023-08-10)


### Bug Fixes

* **chat:** update data keys ([#923](https://github.com/StanGirard/quivr/issues/923)) ([21db719](https://github.com/StanGirard/quivr/commit/21db7197965f1cacd6595ae94d9017fc54d761c3))

## [0.0.55](https://github.com/StanGirard/quivr/compare/v0.0.54...v0.0.55) (2023-08-10)


### Features

* **chatMessages:** add brain_id and prompt_id columns  ([#912](https://github.com/StanGirard/quivr/issues/912)) ([6e77732](https://github.com/StanGirard/quivr/commit/6e777327aaee7b9f35b20dcd00814f4acbaf448e))
* **invitation:** add translations ([#909](https://github.com/StanGirard/quivr/issues/909)) ([1360ce8](https://github.com/StanGirard/quivr/commit/1360ce801d8958defa5dd29a481e2e66ac6ae9ac))
* Russian language translation ([#903](https://github.com/StanGirard/quivr/issues/903)) ([672eec0](https://github.com/StanGirard/quivr/commit/672eec08bc7113e3f4c32a29ae86b2b879262d30))

## [0.0.54](https://github.com/StanGirard/quivr/compare/v0.0.53...v0.0.54) (2023-08-08)


### Features

* add new chat bar ([#896](https://github.com/StanGirard/quivr/issues/896)) ([69a73f5](https://github.com/StanGirard/quivr/commit/69a73f5d5ae58dca9c23c0d8751f8c7326c84f4c))
* add new chat page ([#890](https://github.com/StanGirard/quivr/issues/890)) ([c43e0c0](https://github.com/StanGirard/quivr/commit/c43e0c01c4ddcf0d97b9bb89784ff004fb7a0a79))
* deleting brains on brain manager page ([#893](https://github.com/StanGirard/quivr/issues/893)) ([71e142b](https://github.com/StanGirard/quivr/commit/71e142ba3c164e5f14959cd1fd5de38531779034))


### Bug Fixes

* **es:** spanish translations ([#895](https://github.com/StanGirard/quivr/issues/895)) ([69d0893](https://github.com/StanGirard/quivr/commit/69d08937de1540cf39a6462b4583b2c4c908d0af))
* **sentry:** some unhandled errors ([#894](https://github.com/StanGirard/quivr/issues/894)) ([9ba7241](https://github.com/StanGirard/quivr/commit/9ba724168eacf4b074ad062f2a58b637597335ba))

## [0.0.53](https://github.com/StanGirard/quivr/compare/v0.0.52...v0.0.53) (2023-08-07)


### Features

* **backend:** add custom prompt ([#885](https://github.com/StanGirard/quivr/issues/885)) ([61cd0a6](https://github.com/StanGirard/quivr/commit/61cd0a6bde989bc9f931f47967c3bbddc3b0446b))
* **fr:** added language  ([#884](https://github.com/StanGirard/quivr/issues/884)) ([1160e16](https://github.com/StanGirard/quivr/commit/1160e160141f350a39ae4f73ff88ad79e1b1d874))
* gpt4 is not available for brains if there is no given openAiKey  ([#850](https://github.com/StanGirard/quivr/issues/850)) ([e9ebeef](https://github.com/StanGirard/quivr/commit/e9ebeef72ae2dee40b6bdff58121f9f9e1814577))
* **qa:** improve code ([#886](https://github.com/StanGirard/quivr/issues/886)) ([7028505](https://github.com/StanGirard/quivr/commit/7028505571a8e1f8569a12b770b3ce99cd2ec4e0))


### Bug Fixes

* **i18n:** update tests for french and spanish ([#878](https://github.com/StanGirard/quivr/issues/878)) ([b0514d6](https://github.com/StanGirard/quivr/commit/b0514d6149d474747de642d12454f6b511a1f947))

## [0.0.52](https://github.com/StanGirard/quivr/compare/v0.0.51...v0.0.52) (2023-08-07)


### Features

* add custom prompt fields on brain setting pages ([#837](https://github.com/StanGirard/quivr/issues/837)) ([99a3fa9](https://github.com/StanGirard/quivr/commit/99a3fa9b296520a71028194e21bc808a2ec208a0))
* add public prompts picker ([#841](https://github.com/StanGirard/quivr/issues/841)) ([b3fb8fc](https://github.com/StanGirard/quivr/commit/b3fb8fc3bc2d71a72e73b4f0aa30c84255a77fc0))
* remove private prompts on related brain delete ([#842](https://github.com/StanGirard/quivr/issues/842)) ([4c15fe2](https://github.com/StanGirard/quivr/commit/4c15fe2bfde7a2fdc59c299ef668f1ba0cd8ffa8))


### Bug Fixes

* **pg-database:** by default variable is not implemented ([#848](https://github.com/StanGirard/quivr/issues/848)) ([69e2c28](https://github.com/StanGirard/quivr/commit/69e2c289e5a6e4cfd6b7187a3c4fda5c538d5d35))
* remove typo ([#853](https://github.com/StanGirard/quivr/issues/853)) ([5496e9d](https://github.com/StanGirard/quivr/commit/5496e9d738a1f80f11b6c8fa8606960abcbcd06d))


### Performance Improvements

* **deps:** removed ([#873](https://github.com/StanGirard/quivr/issues/873)) ([10d4d65](https://github.com/StanGirard/quivr/commit/10d4d65c1e203aaae1069395ed5066fbfc9c7715))

## [0.0.51](https://github.com/StanGirard/quivr/compare/v0.0.50...v0.0.51) (2023-08-03)


### Features

* **backend:** implement brain-prompt link ([#831](https://github.com/StanGirard/quivr/issues/831)) ([4ca6c66](https://github.com/StanGirard/quivr/commit/4ca6c667da3d5daf0339c65f077c8956c7ef42e8))
* **prompt:** add prompt table, entity and repository ([#823](https://github.com/StanGirard/quivr/issues/823)) ([e3b6114](https://github.com/StanGirard/quivr/commit/e3b6114248ee04a9dc6b93093256d82324672925))


### Bug Fixes

* **chat routes:** HTTPException import correction ([#833](https://github.com/StanGirard/quivr/issues/833)) ([68f03b2](https://github.com/StanGirard/quivr/commit/68f03b2416f5b49e9f8e72c5b1c91754792a1233))
* **chats:** delete chats from correct table ([#834](https://github.com/StanGirard/quivr/issues/834)) ([659e585](https://github.com/StanGirard/quivr/commit/659e585145ea0aa8bf88ecc48d31e0b65098a729))
* **env:** added pg database url default value to none ([23f50ec](https://github.com/StanGirard/quivr/commit/23f50ec3a37af453f1b8b69592d1a640189d50e8))

## [0.0.50](https://github.com/StanGirard/quivr/compare/v0.0.49...v0.0.50) (2023-08-02)


### Features

* Introduce repository pattern to prepare adding other database providers ([#646](https://github.com/StanGirard/quivr/issues/646)) ([303ba72](https://github.com/StanGirard/quivr/commit/303ba72028d349196b78cc07db627115ec0aff90))
* **prompt:** added instructions in standalone question & a bit more things  ([#826](https://github.com/StanGirard/quivr/issues/826)) ([c217979](https://github.com/StanGirard/quivr/commit/c21797905d7d57dab73f9b7047da1a50aae37b9b))

## [0.0.49](https://github.com/StanGirard/quivr/compare/v0.0.48...v0.0.49) (2023-08-01)


### Features

* add chat config modal ([#807](https://github.com/StanGirard/quivr/issues/807)) ([d018ab6](https://github.com/StanGirard/quivr/commit/d018ab6a9334b45b86e0c7fed3a552f5cb202523))


### Bug Fixes

* bugs ([#818](https://github.com/StanGirard/quivr/issues/818)) ([edcbb30](https://github.com/StanGirard/quivr/commit/edcbb30e97535013b61d5a94bb4204d030cba2f2))

## [0.0.48](https://github.com/StanGirard/quivr/compare/v0.0.47...v0.0.48) (2023-08-01)


### Bug Fixes

* **openai:** user key now used for llm model ([c01433c](https://github.com/StanGirard/quivr/commit/c01433c84194e1d155ad3917de58257d24c30c38))

## [0.0.47](https://github.com/StanGirard/quivr/compare/v0.0.46...v0.0.47) (2023-08-01)


### Features

* add user level open ai key management ([#805](https://github.com/StanGirard/quivr/issues/805)) ([7532b55](https://github.com/StanGirard/quivr/commit/7532b558c74962e5916b951235e8578cc8e882a2))
* **chat:** added streaming ([#808](https://github.com/StanGirard/quivr/issues/808)) ([3166d08](https://github.com/StanGirard/quivr/commit/3166d089ee82730882c26454bd110a3dfae067c9))
* **llm:** removing all llms to prepare for genoss ([#804](https://github.com/StanGirard/quivr/issues/804)) ([db40f3c](https://github.com/StanGirard/quivr/commit/db40f3cccd596f4337823e0306e66224d5e1c8c9))

## [0.0.46](https://github.com/StanGirard/quivr/compare/v0.0.45...v0.0.46) (2023-07-31)


### Features

* **aws:** increased numer of replicas to 10 ([9809ef4](https://github.com/StanGirard/quivr/commit/9809ef4119a2351b78217c73c545b7e327676135))
* **aws:** increased size ([56f254a](https://github.com/StanGirard/quivr/commit/56f254a050fcc3b9ee073318bd566e03675658cd))


### Bug Fixes

* **frontend:** correctly display document information in explore view details ([#781](https://github.com/StanGirard/quivr/issues/781)) ([87c5e58](https://github.com/StanGirard/quivr/commit/87c5e582a2579ebb68f272cb62175dfa6f2e6dc8))
* Toast message hidden under the footer ([#761](https://github.com/StanGirard/quivr/issues/761)) ([3e8ed46](https://github.com/StanGirard/quivr/commit/3e8ed463173659ebe599602e97c2d11191144ecb))
* udpate migration script doc ([#793](https://github.com/StanGirard/quivr/issues/793)) ([a609c01](https://github.com/StanGirard/quivr/commit/a609c01aa8fab10e74eed64edd795c56bece1fdb))

## [0.0.45](https://github.com/StanGirard/quivr/compare/v0.0.44...v0.0.45) (2023-07-27)


### Bug Fixes

* **release-please:** use personal token to be able to trigger release ([#789](https://github.com/StanGirard/quivr/issues/789)) ([2fcff0b](https://github.com/StanGirard/quivr/commit/2fcff0bedab3a53cb3dc395c0e362edb2962aaa7))

## [0.0.44](https://github.com/StanGirard/quivr/compare/v0.0.43...v0.0.44) (2023-07-27)


### Features

* **pr-title:** added pr-title checlk ([b11b2d8](https://github.com/StanGirard/quivr/commit/b11b2d8658fec3940bb0c0280124cbdd77d8d74b))


### Bug Fixes

* **release-please:** fixed actions ([16114b2](https://github.com/StanGirard/quivr/commit/16114b2c5271ab299b7e84f5a9e552dab58cd211))

## [0.0.43](https://github.com/StanGirard/quivr/compare/v0.0.42...v0.0.43) (2023-07-26)


### Features

* **workflow:** added release please ([e6ba9e8](https://github.com/StanGirard/quivr/commit/e6ba9e80f48a1d8822c99e5b77e064dc2b18e718))
