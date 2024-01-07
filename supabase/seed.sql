SET session_replication_role = replica;
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Ubuntu 15.1-1.pgdg20.04+1)
-- Dumped by pg_dump version 15.5 (Ubuntu 15.5-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."audit_log_entries" ("instance_id", "id", "payload", "created_at", "ip_address") VALUES
	('00000000-0000-0000-0000-000000000000', '479f1b0e-4e73-4a73-9b0a-349cfc333215', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"user_email":"admin@quivr.app","user_id":"d777f5d2-1494-460c-82b4-70f445b6344b","user_phone":""}}', '2024-01-03 17:52:45.895193+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b21c9ed5-6a11-4da6-b0ba-86a84ae01d9d', '{"action":"login","actor_id":"d777f5d2-1494-460c-82b4-70f445b6344b","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2024-01-03 17:57:52.722055+00', ''),
	('00000000-0000-0000-0000-000000000000', 'f7fbe861-c477-483e-a74a-8dcb9f2df8c5', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"user_email":"admin@quivr.app","user_id":"bad271c8-973a-4dcc-8e87-1de818ea1234","user_phone":""}}', '2024-01-03 17:59:11.223649+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ab775301-f67a-4006-91ab-2c8699e167d6', '{"action":"login","actor_id":"bad271c8-973a-4dcc-8e87-1de818ea1234","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2024-01-04 11:18:23.477505+00', ''),
	('00000000-0000-0000-0000-000000000000', '3f11e765-1d89-4b91-a38a-172bf1742d84', '{"action":"token_refreshed","actor_id":"bad271c8-973a-4dcc-8e87-1de818ea1234","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-01-04 12:35:08.151537+00', ''),
	('00000000-0000-0000-0000-000000000000', '60e6d71d-0439-47ac-a2c8-c145802e1819', '{"action":"token_revoked","actor_id":"bad271c8-973a-4dcc-8e87-1de818ea1234","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-01-04 12:35:08.154258+00', ''),
	('00000000-0000-0000-0000-000000000000', '86cad64b-6270-42c3-b94c-48f8bb06a552', '{"action":"token_refreshed","actor_id":"bad271c8-973a-4dcc-8e87-1de818ea1234","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-01-04 12:35:08.388275+00', '');


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at") VALUES
	('00000000-0000-0000-0000-000000000000', 'bad271c8-973a-4dcc-8e87-1de818ea1234', 'authenticated', 'authenticated', 'admin@quivr.app', '$2a$10$fo99ZlLdOex9QJy5cMN8OuQD2EBylfB1dPCfdLeXniDr6a6K1jOEu', '2024-01-03 17:59:11.22809+00', NULL, '', NULL, '', NULL, '', '', NULL, '2024-01-04 11:18:23.483783+00', '{"provider": "email", "providers": ["email"]}', '{}', NULL, '2024-01-03 17:59:11.212675+00', '2024-01-04 12:35:08.161692+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL);


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."identities" ("provider_id", "user_id", "identity_data", "provider", "last_sign_in_at", "created_at", "updated_at", "id") VALUES
	('bad271c8-973a-4dcc-8e87-1de818ea1234', 'bad271c8-973a-4dcc-8e87-1de818ea1234', '{"sub": "bad271c8-973a-4dcc-8e87-1de818ea1234", "email": "admin@quivr.app", "email_verified": false, "phone_verified": false}', 'email', '2024-01-03 17:59:11.222255+00', '2024-01-03 17:59:11.222367+00', '2024-01-03 17:59:11.222367+00', 'b22ef918-7d7c-4d30-b51a-0ac15a25ae0c');


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."sessions" ("id", "user_id", "created_at", "updated_at", "factor_id", "aal", "not_after", "refreshed_at", "user_agent", "ip", "tag") VALUES
	('24633b5b-1c98-46d1-b77b-f6f26f3fbed8', 'bad271c8-973a-4dcc-8e87-1de818ea1234', '2024-01-04 11:18:23.484077+00', '2024-01-04 12:35:08.389426+00', NULL, 'aal1', NULL, '2024-01-04 12:35:08.389371', 'node', '192.168.65.1', NULL);


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."mfa_amr_claims" ("session_id", "created_at", "updated_at", "authentication_method", "id") VALUES
	('24633b5b-1c98-46d1-b77b-f6f26f3fbed8', '2024-01-04 11:18:23.505534+00', '2024-01-04 11:18:23.505534+00', 'password', '8c4b5bd7-0598-49ef-b250-edd41ffe3ae6');


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."refresh_tokens" ("instance_id", "id", "token", "user_id", "revoked", "created_at", "updated_at", "parent", "session_id") VALUES
	('00000000-0000-0000-0000-000000000000', 2, 'KZtTz92zaQCDqfYGVxdbpw', 'bad271c8-973a-4dcc-8e87-1de818ea1234', true, '2024-01-04 11:18:23.491804+00', '2024-01-04 12:35:08.154709+00', NULL, '24633b5b-1c98-46d1-b77b-f6f26f3fbed8'),
	('00000000-0000-0000-0000-000000000000', 3, 'NKBFXjIleRD_NS0NslmLMA', 'bad271c8-973a-4dcc-8e87-1de818ea1234', false, '2024-01-04 12:35:08.159711+00', '2024-01-04 12:35:08.159711+00', 'KZtTz92zaQCDqfYGVxdbpw', '24633b5b-1c98-46d1-b77b-f6f26f3fbed8');


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: prompts; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: brains; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."brains" ("brain_id", "name", "status", "model", "max_tokens", "temperature", "description", "prompt_id", "last_update", "brain_type", "openai_api_key") VALUES
	('ba005f96-ca14-496c-ac97-07bfea3ce200', 'Default brain', 'private', NULL, 256, 0, 'This is a description', NULL, '2024-01-04 11:18:24.87015', 'doc', NULL);


--
-- Data for Name: api_brain_definition; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: api_keys; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."api_keys" ("key_id", "user_id", "api_key", "creation_time", "deleted_time", "is_active", "name", "days", "only_chat") VALUES
	('46410f65-fad1-4f2c-b931-259dd449059d', 'bad271c8-973a-4dcc-8e87-1de818ea1234', '72768a722efc7585d0be4ff6adcfe80b', '2024-01-04 13:03:49', NULL, true, 'api_key', 30, false);


--
-- Data for Name: brain_subscription_invitations; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: brains_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."brains_users" ("brain_id", "rights", "default_brain", "user_id") VALUES
	('ba005f96-ca14-496c-ac97-07bfea3ce200', 'Owner', true, 'bad271c8-973a-4dcc-8e87-1de818ea1234');


--
-- Data for Name: vectors; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: brains_vectors; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: chats; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."chats" ("chat_id", "user_id", "creation_time", "history", "chat_name") VALUES
	('26775754-f3e7-4038-8308-bd3f4319a880', 'bad271c8-973a-4dcc-8e87-1de818ea1234', '2024-01-04 11:18:33.973348', NULL, 'test'),
	('2783a01c-a3ab-416d-9956-e21c3fbf723f', 'bad271c8-973a-4dcc-8e87-1de818ea1234', '2024-01-04 11:22:03.683517', NULL, 'test'),
	('af673c10-6556-49c2-9824-a829c4611acc', 'bad271c8-973a-4dcc-8e87-1de818ea1234', '2024-01-04 11:26:12.298316', NULL, 'Test'),
	('4b05acf1-8ac8-4068-98d5-232f665e1cb7', 'bad271c8-973a-4dcc-8e87-1de818ea1234', '2024-01-04 12:37:50.554177', NULL, 'Hello'),
	('7ba13242-0f8d-4eda-af3a-324c7ed99d16', 'bad271c8-973a-4dcc-8e87-1de818ea1234', '2024-01-04 12:50:13.583812', NULL, 'Hello');


--
-- Data for Name: chat_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."chat_history" ("message_id", "chat_id", "user_message", "assistant", "message_time", "brain_id", "prompt_id") VALUES
	('b93d0e01-3711-4b1f-aca0-e2800af363a4', '26775754-f3e7-4038-8308-bd3f4319a880', 'test', 'Hello! How can I assist you today?', '2024-01-04 11:19:56.585019', NULL, NULL),
	('332a88f0-fc37-4308-b4d1-524f2c69b7e9', 'af673c10-6556-49c2-9824-a829c4611acc', 'Test', 'Hello! How can I assist you today?', '2024-01-04 11:26:12.48397', NULL, NULL),
	('4e75ab6c-8a32-4b06-bb15-8b043c6625dd', '4b05acf1-8ac8-4068-98d5-232f665e1cb7', 'Hello', 'Hello! How can I assist you today?', '2024-01-04 12:37:52.777877', NULL, NULL),
	('448c922d-0b48-435c-92b8-0cbc71497f9a', '7ba13242-0f8d-4eda-af3a-324c7ed99d16', 'Hello', 'Hello! How can I assist you today?', '2024-01-04 12:50:15.886321', NULL, NULL);


--
-- Data for Name: composite_brain_connections; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: knowledge; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: knowledge_vectors; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: models; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."models" ("name", "price", "max_input", "max_output") VALUES
	('gpt-3.5-turbo-1106', 1, 2000, 1000),
	('ollama/llama2', 1, 2000, 1000);


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: onboardings; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."onboardings" ("user_id", "onboarding_a", "onboarding_b1", "onboarding_b2", "onboarding_b3", "creation_time") VALUES
	('bad271c8-973a-4dcc-8e87-1de818ea1234', true, true, true, true, '2024-01-03 17:59:11.212049');


--
-- Data for Name: product_to_features; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: stats; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: summaries; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: user_daily_usage; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."user_daily_usage" ("user_id", "email", "date", "daily_requests_count") VALUES
	('bad271c8-973a-4dcc-8e87-1de818ea1234', 'admin@quivr.app', '20240104', 4);


--
-- Data for Name: user_identity; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."user_identity" ("user_id", "openai_api_key") VALUES
	('bad271c8-973a-4dcc-8e87-1de818ea1234', NULL);


--
-- Data for Name: user_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."user_settings" ("user_id", "models", "daily_chat_credit", "max_brains", "max_brain_size", "is_premium", "api_access") VALUES
	('bad271c8-973a-4dcc-8e87-1de818ea1234', '["gpt-3.5-turbo-1106"]', 20, 3, 50000000, true, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."users" ("id", "email") VALUES
	('bad271c8-973a-4dcc-8e87-1de818ea1234', 'admin@quivr.app');


--
-- Data for Name: users_old; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: vectors_old; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 3, true);



--
-- Name: product_to_features_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."product_to_features_id_seq"', 1, false);





--
-- PostgreSQL database dump complete
--

RESET ALL;
