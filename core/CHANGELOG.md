# Changelog

## [0.0.34](https://github.com/QuivrHQ/quivr/compare/core-0.0.33...core-0.0.34) (2025-06-19)


### Features

* add default values for GPT-4.1  ([#3641](https://github.com/QuivrHQ/quivr/issues/3641)) ([e48ff2f](https://github.com/QuivrHQ/quivr/commit/e48ff2f723cd44f3970ae385b862dd5dd73de53c))
* add filters ([#3621](https://github.com/QuivrHQ/quivr/issues/3621)) ([1707f18](https://github.com/QuivrHQ/quivr/commit/1707f18e3923ae7e32ecdbd38380434ee71df7d7))
* Add Gemini support for language models ([#3632](https://github.com/QuivrHQ/quivr/issues/3632)) ([add322c](https://github.com/QuivrHQ/quivr/commit/add322c8d6c3ee8cd712dface19fa615a4980cac))
* add guidelines ([#3613](https://github.com/QuivrHQ/quivr/issues/3613)) ([6f99bd3](https://github.com/QuivrHQ/quivr/commit/6f99bd32e222093051eb9e3ce89050a198262438))
* add langchain-groq dependency and update LLMEndpoint to use ChatGroq ([#3633](https://github.com/QuivrHQ/quivr/issues/3633)) ([3556477](https://github.com/QuivrHQ/quivr/commit/3556477993a8f3bbfab5d4a5e119a447d027bc61))
* add run-id langfuse ([#3629](https://github.com/QuivrHQ/quivr/issues/3629)) ([f8298c1](https://github.com/QuivrHQ/quivr/commit/f8298c1311685732fc36d4381f1188c239277035))
* add system_prompt parameter to Brain methods and enhance message handling in RAG pipeline ([#3625](https://github.com/QuivrHQ/quivr/issues/3625)) ([500d793](https://github.com/QuivrHQ/quivr/commit/500d7931582d4329044315b21675d1535ebcdcac))
* add zendesk llm template for reformulate ([#3619](https://github.com/QuivrHQ/quivr/issues/3619)) ([e4140d5](https://github.com/QuivrHQ/quivr/commit/e4140d5c32d18b999543c5307770c3ed23ae4cc1))
* additional-data ([#3614](https://github.com/QuivrHQ/quivr/issues/3614)) ([f9c05f9](https://github.com/QuivrHQ/quivr/commit/f9c05f98f2c8cb26407a8946d81e02a683abc585))
* arbitrary additional data for zendesk ([#3612](https://github.com/QuivrHQ/quivr/issues/3612)) ([1a05434](https://github.com/QuivrHQ/quivr/commit/1a05434207e05a8358984af5181194d19c517023))
* cache llm endpoint ([#3635](https://github.com/QuivrHQ/quivr/issues/3635)) ([5bc8b56](https://github.com/QuivrHQ/quivr/commit/5bc8b561081474dd44134b34c656f5b4e46bba6b))
* core input metadata zendesk ([#3606](https://github.com/QuivrHQ/quivr/issues/3606)) ([855a791](https://github.com/QuivrHQ/quivr/commit/855a791f0fda8d2d603c79fdbd11e1add81c1a09)), closes [#3602](https://github.com/QuivrHQ/quivr/issues/3602)
* enhance zendesk template with clearer guidelines and instructions ([#3624](https://github.com/QuivrHQ/quivr/issues/3624)) ([d378478](https://github.com/QuivrHQ/quivr/commit/d37847807da28a7140281436a13f2d3f53eb1880))
* fix chat with model ([#3615](https://github.com/QuivrHQ/quivr/issues/3615)) ([22c740b](https://github.com/QuivrHQ/quivr/commit/22c740b9a3b299a158120a3d8b6da90f45bed48d))
* include current time in prompt context and improve assertion formatting in QuivrQARAGLangGraph ([4532bb6](https://github.com/QuivrHQ/quivr/commit/4532bb6dedfa2161238ffc5afff8981bb8da06ea))
* megaparse v54 ([#3594](https://github.com/QuivrHQ/quivr/issues/3594)) ([bc6d75d](https://github.com/QuivrHQ/quivr/commit/bc6d75df7348294bc5cde4409d7c17feb72cf2b2))
* metadata brain core ([ce95a3a](https://github.com/QuivrHQ/quivr/commit/ce95a3a18f472f777e0ba9dbecdb400332815948))
* refine response instructions in client query prompt ([e391817](https://github.com/QuivrHQ/quivr/commit/e391817f58bf7f4be6bc4a00ac570cdfc34de784))
* renamed system_prompt to correct naming ([#3622](https://github.com/QuivrHQ/quivr/issues/3622)) ([3db473f](https://github.com/QuivrHQ/quivr/commit/3db473fe913f4d7d8049523ec3f9e0022840b6e6))


### Bug Fixes

* 2: Historic is now added ([5dd44d8](https://github.com/QuivrHQ/quivr/commit/5dd44d8eb37b25e9d7c14c14df47f19849cdd031))
* add Claude 4 support ([#3645](https://github.com/QuivrHQ/quivr/issues/3645)) ([947a785](https://github.com/QuivrHQ/quivr/commit/947a785415c6c35ab2ae8157222b4720b0710b4d))
* add system prompt to zendesk rag ([#3604](https://github.com/QuivrHQ/quivr/issues/3604)) ([501783b](https://github.com/QuivrHQ/quivr/commit/501783b53cf3751c0c9a48f2fcacc933fb4f161d))
* **brain:** pass missing run_id ([#3631](https://github.com/QuivrHQ/quivr/issues/3631)) ([4f0fb6f](https://github.com/QuivrHQ/quivr/commit/4f0fb6f4c352585f9621eb8a588b28813eb96232))
* coquille grok to groq ([3556477](https://github.com/QuivrHQ/quivr/commit/3556477993a8f3bbfab5d4a5e119a447d027bc61))
* ENT-673 ([501783b](https://github.com/QuivrHQ/quivr/commit/501783b53cf3751c0c9a48f2fcacc933fb4f161d))
* ENT-716 ([6f99bd3](https://github.com/QuivrHQ/quivr/commit/6f99bd32e222093051eb9e3ce89050a198262438))
* fix grammar and typo in zendesk prompte template ([#3628](https://github.com/QuivrHQ/quivr/issues/3628)) ([2898a5d](https://github.com/QuivrHQ/quivr/commit/2898a5d511f826cbdca50e49ec0fa26e8cd27122))
* format prompt for zendesk ([#3627](https://github.com/QuivrHQ/quivr/issues/3627)) ([df2d345](https://github.com/QuivrHQ/quivr/commit/df2d345f550d9e79a6522bdc16bbbf28731fd08a))
* historic and iterate ([#3642](https://github.com/QuivrHQ/quivr/issues/3642)) ([5dd44d8](https://github.com/QuivrHQ/quivr/commit/5dd44d8eb37b25e9d7c14c14df47f19849cdd031))
* prompts to ensure correct formatting ([#3636](https://github.com/QuivrHQ/quivr/issues/3636)) ([62a8585](https://github.com/QuivrHQ/quivr/commit/62a8585037680cda809022c3543c690fa98571df))
* Zendesk system prompt ([#3592](https://github.com/QuivrHQ/quivr/issues/3592)) ([699b549](https://github.com/QuivrHQ/quivr/commit/699b5495f5519e79fd2a6d0e362402c3c77d06b8))

## [0.0.33](https://github.com/QuivrHQ/quivr/compare/core-0.0.32...core-0.0.33) (2025-02-03)


### Features

* **zendesk:** add zendesk workflow ([#3586](https://github.com/QuivrHQ/quivr/issues/3586)) ([ee9b7a5](https://github.com/QuivrHQ/quivr/commit/ee9b7a5740825bd3fc9186e0a9179959c6525e5e))


### Bug Fixes

* CLI-24 ([ee9b7a5](https://github.com/QuivrHQ/quivr/commit/ee9b7a5740825bd3fc9186e0a9179959c6525e5e))

## [0.0.32](https://github.com/QuivrHQ/quivr/compare/core-0.0.31...core-0.0.32) (2025-01-31)


### Features

* o3-mini ([#3583](https://github.com/QuivrHQ/quivr/issues/3583)) ([a639e0c](https://github.com/QuivrHQ/quivr/commit/a639e0ce50297e0fefa809b7edb57b50863b446d))

## [0.0.31](https://github.com/QuivrHQ/quivr/compare/core-0.0.30...core-0.0.31) (2025-01-30)


### Features

* cache tokenizers ([#3558](https://github.com/QuivrHQ/quivr/issues/3558)) ([699dc2e](https://github.com/QuivrHQ/quivr/commit/699dc2e187abc9986845f591111723088f5bcefe))
* limit tokenizers cache size ([#3577](https://github.com/QuivrHQ/quivr/issues/3577)) ([e2a3bcb](https://github.com/QuivrHQ/quivr/commit/e2a3bcbbdb469348187d986de9ba3901938bed58))
* remove pympler dependency and add better way to calculate size of tokenizer cache ([#3580](https://github.com/QuivrHQ/quivr/issues/3580)) ([2fbd5d4](https://github.com/QuivrHQ/quivr/commit/2fbd5d48443625dd3fe8a37c04275cd760e7285f))
* remove tokenizer load ([#3576](https://github.com/QuivrHQ/quivr/issues/3576)) ([05e212a](https://github.com/QuivrHQ/quivr/commit/05e212a30929ba3c00e31e3364363eb4a4376ad9))

## [0.0.30](https://github.com/QuivrHQ/quivr/compare/core-0.0.29...core-0.0.30) (2025-01-27)


### Features

* adding cache to LLMEndpoint ([#3555](https://github.com/QuivrHQ/quivr/issues/3555)) ([6072907](https://github.com/QuivrHQ/quivr/commit/6072907ca7370be748d2d6845fd674abbb6c83c3))

## [0.0.29](https://github.com/QuivrHQ/quivr/compare/core-0.0.28...core-0.0.29) (2025-01-20)


### Features

* enabling workflows without rewriting step ([#3549](https://github.com/QuivrHQ/quivr/issues/3549)) ([bbe1c18](https://github.com/QuivrHQ/quivr/commit/bbe1c183768bf32945554e679cab737c07bb3dde))
* improving the prompts to always refer to 'tasks' instead of 'questions' ([#3528](https://github.com/QuivrHQ/quivr/issues/3528)) ([e9c72e1](https://github.com/QuivrHQ/quivr/commit/e9c72e15671407290f1a3a9758bf38a3357d2b15))
* langfuse integration ([#3530](https://github.com/QuivrHQ/quivr/issues/3530)) ([c4aae1a](https://github.com/QuivrHQ/quivr/commit/c4aae1a6c21fd7bc7019676d32fa5b2e8fbbe171))
* langfuse user id ([#3533](https://github.com/QuivrHQ/quivr/issues/3533)) ([e0ccd3d](https://github.com/QuivrHQ/quivr/commit/e0ccd3dc04b7527b27520465b2cf179e9789bf3f))
* language detection after chunking ([#3532](https://github.com/QuivrHQ/quivr/issues/3532)) ([d0adb81](https://github.com/QuivrHQ/quivr/commit/d0adb8112a27fb7f25564d328a6f7e50ba27ba3a))
* returning a description of each workflow node ([#3539](https://github.com/QuivrHQ/quivr/issues/3539)) ([d835fc6](https://github.com/QuivrHQ/quivr/commit/d835fc6e4c062bd485a715bc707a902493e092c2))


### Bug Fixes

* langfuse talk to model ([#3535](https://github.com/QuivrHQ/quivr/issues/3535)) ([9681a9e](https://github.com/QuivrHQ/quivr/commit/9681a9ec8b6b09fe20d04bf41d17a57afc5398f9))

## [0.0.28](https://github.com/QuivrHQ/quivr/compare/core-0.0.27...core-0.0.28) (2024-12-17)


### Features

* remove dependencies on Pydantic v1 ([#3526](https://github.com/QuivrHQ/quivr/issues/3526)) ([ebc4eb8](https://github.com/QuivrHQ/quivr/commit/ebc4eb811c258ce0500032bbc52d96f333fabf89))

## [0.0.27](https://github.com/QuivrHQ/quivr/compare/core-0.0.26...core-0.0.27) (2024-12-16)


### Features

* ensuring that max_context_tokens is never larger than what supported by models ([#3519](https://github.com/QuivrHQ/quivr/issues/3519)) ([d6e0ed4](https://github.com/QuivrHQ/quivr/commit/d6e0ed44df0ee7edafea85f704a15fd99969bafd))
* send all to megaparse_sdk ([#3521](https://github.com/QuivrHQ/quivr/issues/3521)) ([e48044d](https://github.com/QuivrHQ/quivr/commit/e48044d36ffda613f65da24641ed8da290195177))


### Bug Fixes

* fixing errors arising when the user input contains no tasks ([#3525](https://github.com/QuivrHQ/quivr/issues/3525)) ([e28f7bc](https://github.com/QuivrHQ/quivr/commit/e28f7bcb9ab9534bc011664525ae1f9c2cf6393e))

## [0.0.26](https://github.com/QuivrHQ/quivr/compare/core-0.0.25...core-0.0.26) (2024-12-10)


### Features

* first version (V0) of the Workflow Management System ([#3493](https://github.com/QuivrHQ/quivr/issues/3493)) ([6450a49](https://github.com/QuivrHQ/quivr/commit/6450a494e3efa8e8c267ca49aa0a7ec682586b4e))


### Bug Fixes

* dealing with empty tool_calls ([#3514](https://github.com/QuivrHQ/quivr/issues/3514)) ([e2f6389](https://github.com/QuivrHQ/quivr/commit/e2f6389189d911a382b2236ab39f28a1270528ac))

## [0.0.25](https://github.com/QuivrHQ/quivr/compare/core-0.0.24...core-0.0.25) (2024-11-28)


### Bug Fixes

* megaparse sdk with nats ([#3496](https://github.com/QuivrHQ/quivr/issues/3496)) ([e68b4f4](https://github.com/QuivrHQ/quivr/commit/e68b4f45698898f6b514d4779c8e5fd7332f2e67))


### Documentation

* Enhance example/chatbot with added instructions ([#3506](https://github.com/QuivrHQ/quivr/issues/3506)) ([d1d608d](https://github.com/QuivrHQ/quivr/commit/d1d608d19ffb9213910575981eff3527f7d232a0))

## [0.0.24](https://github.com/QuivrHQ/quivr/compare/core-0.0.23...core-0.0.24) (2024-11-14)


### Features

* kms-migration ([#3446](https://github.com/QuivrHQ/quivr/issues/3446)) ([1356d87](https://github.com/QuivrHQ/quivr/commit/1356d87098ae84776a5d47b631d07a1c8e92e291))
* **megaparse:** add sdk ([#3462](https://github.com/QuivrHQ/quivr/issues/3462)) ([190d971](https://github.com/QuivrHQ/quivr/commit/190d971bd71333924b88ba747d3c6a833ca65d92))


### Bug Fixes

* added chunk_size in tika processor ([#3466](https://github.com/QuivrHQ/quivr/issues/3466)) ([063bbd3](https://github.com/QuivrHQ/quivr/commit/063bbd323dfca2dfc22fc5416c1617ed61d2e2ab))
* modify megaparse strategy ([#3474](https://github.com/QuivrHQ/quivr/issues/3474)) ([da97b2c](https://github.com/QuivrHQ/quivr/commit/da97b2cf145c86ed577be698ae837b3dc26f6921))
* supported extensions for megaparse ([#3477](https://github.com/QuivrHQ/quivr/issues/3477)) ([72b979d](https://github.com/QuivrHQ/quivr/commit/72b979d4e4d6e6efc45d47c7aba942eb909adc3e))

## [0.0.23](https://github.com/QuivrHQ/quivr/compare/core-0.0.22...core-0.0.23) (2024-10-31)


### Features

* websearch, tool use, user intent, dynamic retrieval, multiple questions ([#3424](https://github.com/QuivrHQ/quivr/issues/3424)) ([285fe5b](https://github.com/QuivrHQ/quivr/commit/285fe5b96065a19c74f0314557e5840d8722099e))

## [0.0.22](https://github.com/QuivrHQ/quivr/compare/core-0.0.21...core-0.0.22) (2024-10-21)


### Features

* **ask:** non-streaming now calls streaming ([#3409](https://github.com/QuivrHQ/quivr/issues/3409)) ([e71e46b](https://github.com/QuivrHQ/quivr/commit/e71e46bcdfbab0d583aef015604278343fd46c6f))

## [0.0.21](https://github.com/QuivrHQ/quivr/compare/core-0.0.20...core-0.0.21) (2024-10-21)


### Features

* **ci:** trigger ([b92774a](https://github.com/QuivrHQ/quivr/commit/b92774aa37ad2051b197daa29fe4b94d57a19986))

## [0.0.20](https://github.com/QuivrHQ/quivr/compare/core-0.0.19...core-0.0.20) (2024-10-21)


### Features

* **ci:** trigger ([#3403](https://github.com/QuivrHQ/quivr/issues/3403)) ([68c09fc](https://github.com/QuivrHQ/quivr/commit/68c09fce85364432da2641d0a8da867516142553))
* **docs:** trigger ci ([5644596](https://github.com/QuivrHQ/quivr/commit/56445967252eac20d17bebc4484d7c00c45d9238))

## [0.0.19](https://github.com/QuivrHQ/quivr/compare/core-0.0.18...core-0.0.19) (2024-10-21)


### Features

* **quivr-core:** beginning ([#3388](https://github.com/QuivrHQ/quivr/issues/3388)) ([7acb52a](https://github.com/QuivrHQ/quivr/commit/7acb52a9637b74d53f3e4cc9dde4ae1ca3f481ad))

## [0.0.18](https://github.com/QuivrHQ/quivr/compare/core-0.0.17...core-0.0.18) (2024-10-16)


### Bug Fixes

* **core:** megaparse config ([#3384](https://github.com/QuivrHQ/quivr/issues/3384)) ([ffe86ca](https://github.com/QuivrHQ/quivr/commit/ffe86ca7bac3d7800913937314170db6f91daf8e))

## [0.0.17](https://github.com/QuivrHQ/quivr/compare/core-0.0.16...core-0.0.17) (2024-10-16)


### Features

* **assistant:** cdp ([#3305](https://github.com/QuivrHQ/quivr/issues/3305)) ([b767f19](https://github.com/QuivrHQ/quivr/commit/b767f19f28b5478cef077b5d1587bf5195f2a668))
* **assistants:** mock api ([#3195](https://github.com/QuivrHQ/quivr/issues/3195)) ([282fa0e](https://github.com/QuivrHQ/quivr/commit/282fa0e3f83f7c6fc8c84ca95f8f4ced4ed34b78))
* introducing configurable retrieval workflows ([#3227](https://github.com/QuivrHQ/quivr/issues/3227)) ([ef90e8e](https://github.com/QuivrHQ/quivr/commit/ef90e8e672ca23d104c7d5bde7496f0929adf5d2))


### Bug Fixes

* fixing pdf parsing ([#3349](https://github.com/QuivrHQ/quivr/issues/3349)) ([367242a](https://github.com/QuivrHQ/quivr/commit/367242a3d5ea2df1928cb2908ad9e1906d1bba6f))


### Documentation

* **core:** init ([#3365](https://github.com/QuivrHQ/quivr/issues/3365)) ([bb572a2](https://github.com/QuivrHQ/quivr/commit/bb572a2a8d060f147461506aadd38704eb029a9a))
* **fix:** fixed warnings from griffe ([#3381](https://github.com/QuivrHQ/quivr/issues/3381)) ([1a38798](https://github.com/QuivrHQ/quivr/commit/1a3879839a2d9e0881e18cb66809564fb76724ef))

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
