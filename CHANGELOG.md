# Changelog

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
