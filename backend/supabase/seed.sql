SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Ubuntu 15.1-1.pgdg20.04+1)
-- Dumped by pg_dump version 15.6 (Ubuntu 15.6-1.pgdg20.04+1)

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
	('00000000-0000-0000-0000-000000000000', '84e89c28-6f5f-4e24-a03b-68cdaa90b3f2', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"user_email":"admin@quivr.app","user_id":"39418e3b-0258-4452-af60-7acfcc1263ff","user_phone":""}}', '2024-01-22 22:27:00.164777+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ac1d43e6-2b2a-4af1-bdd1-c03907e7ba5a', '{"action":"login","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2024-01-22 22:27:50.16388+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e86de23b-ea26-408e-8e8c-a97d2f1f259c', '{"action":"login","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2024-02-06 04:08:08.378325+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a356df58-6d1b-45dd-ae13-08ea7b7a0aff', '{"action":"login","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2024-02-21 02:17:19.558786+00', ''),
	('00000000-0000-0000-0000-000000000000', '8a1ff5f6-5426-4f4b-94ac-d780f6308a8d', '{"action":"logout","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account"}', '2024-03-05 16:11:51.53268+00', ''),
	('00000000-0000-0000-0000-000000000000', '798fde42-d617-4dfd-bf0c-4a6e15dbadbf', '{"action":"login","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2024-03-05 16:12:06.445094+00', ''),
	('00000000-0000-0000-0000-000000000000', '73331e6e-2e66-4db6-816b-980ce65a2481', '{"action":"user_recovery_requested","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"user"}', '2024-03-05 16:22:13.777822+00', ''),
	('00000000-0000-0000-0000-000000000000', 'dcdc846a-7194-4ee4-869e-0c05c269bd75', '{"action":"login","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2024-03-30 23:21:12.07649+00', ''),
	('00000000-0000-0000-0000-000000000000', '3cb1aa8a-bbcf-4871-b9f1-ae3c8a1e7897', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-03-31 00:39:12.712906+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b742a419-21c6-4a89-b966-5fcb44d74ce6', '{"action":"token_revoked","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-03-31 00:39:12.714476+00', ''),
	('00000000-0000-0000-0000-000000000000', '7f37fc2f-4122-4b7d-9be5-8e0e5c217d1b', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-03-31 00:39:12.750952+00', ''),
	('00000000-0000-0000-0000-000000000000', '3a20a51b-0b9b-4fd2-88bb-baf0bd0256e7', '{"action":"token_revoked","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-03-31 00:39:12.751734+00', ''),
	('00000000-0000-0000-0000-000000000000', '7abd9db8-feaa-4286-91ce-f83f26e6248f', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-01 17:40:15.324815+00', ''),
	('00000000-0000-0000-0000-000000000000', '60cbbae4-8f7d-424a-bff9-52f36a3cec18', '{"action":"token_revoked","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-01 17:40:15.327436+00', ''),
	('00000000-0000-0000-0000-000000000000', '8fa8d8cc-069a-4937-9381-f4e0c2014cee', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-01 17:40:29.606995+00', ''),
	('00000000-0000-0000-0000-000000000000', 'c6b4b0f9-6f7c-4e99-b615-19dcc93344bc', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"user_email":"stan@quivr.app","user_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","user_phone":""}}', '2024-04-01 18:33:18.58257+00', ''),
	('00000000-0000-0000-0000-000000000000', '9996a09d-f340-4d8a-8121-1c61678a0035', '{"action":"logout","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account"}', '2024-04-01 18:33:27.294395+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a9e1b230-fcff-4bb7-97ee-99268a8004e5', '{"action":"login","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2024-04-01 18:33:48.194838+00', ''),
	('00000000-0000-0000-0000-000000000000', '227ba305-48e0-4b35-bdf3-1e85dec2b5ff', '{"action":"token_refreshed","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-01 22:57:02.635248+00', ''),
	('00000000-0000-0000-0000-000000000000', '42778009-b9f3-4f5a-b7d9-969180d2e018', '{"action":"token_revoked","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-01 22:57:02.638784+00', ''),
	('00000000-0000-0000-0000-000000000000', '777a94af-6b4f-4f25-b52b-7e8df2986f9b', '{"action":"token_refreshed","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-01 22:57:03.019661+00', ''),
	('00000000-0000-0000-0000-000000000000', '79ba8a24-2851-4027-97ae-257779dd3730', '{"action":"token_refreshed","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-02 00:29:49.500124+00', ''),
	('00000000-0000-0000-0000-000000000000', '0a936f39-4621-41b9-840a-29d8910a3a01', '{"action":"token_revoked","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-02 00:29:49.507212+00', ''),
	('00000000-0000-0000-0000-000000000000', '4b211d7b-3204-409a-9d01-89912527445f', '{"action":"token_refreshed","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-02 00:29:49.532939+00', ''),
	('00000000-0000-0000-0000-000000000000', 'bdf19c9f-51ee-4068-8b1d-844c99409c53', '{"action":"token_revoked","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-02 00:29:49.533754+00', ''),
	('00000000-0000-0000-0000-000000000000', '381c44bf-c4b1-4a1c-ac1d-b17b8881c703', '{"action":"token_refreshed","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-02 01:28:09.342118+00', ''),
	('00000000-0000-0000-0000-000000000000', 'f376cacc-43f2-440d-a048-c19d1aa6373b', '{"action":"token_revoked","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-04-02 01:28:09.345574+00', ''),
	('00000000-0000-0000-0000-000000000000', '7bc1f624-8cd0-4fab-8202-540e5e5a43c6', '{"action":"logout","actor_id":"39a23896-40b9-45cb-8a2c-6223c48e4b35","actor_username":"stan@quivr.app","actor_via_sso":false,"log_type":"account"}', '2024-04-02 01:34:52.219229+00', ''),
	('00000000-0000-0000-0000-000000000000', '25f4ab88-0c60-46ad-a4e1-7d2f7afbc98c', '{"action":"login","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2024-06-24 21:00:12.944793+00', ''),
	('00000000-0000-0000-0000-000000000000', '88b54e13-fd62-4a7d-acb7-61c1de4e0b1f', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-25 14:56:06.210946+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b66a8309-6ba6-470a-a6a0-a158983fdb9e', '{"action":"token_revoked","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-25 14:56:06.214034+00', ''),
	('00000000-0000-0000-0000-000000000000', '2396f6a9-520b-4ac4-b4c0-4a7a29106c63', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-25 14:56:06.423578+00', ''),
	('00000000-0000-0000-0000-000000000000', '98435580-7f70-4068-a4a8-6256c60c89e8', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-25 16:00:34.788918+00', ''),
	('00000000-0000-0000-0000-000000000000', '435037b9-1ec7-45de-80f7-b2af5907c9c3', '{"action":"token_revoked","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-25 16:00:34.790141+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a9c7aeae-503b-40a7-87d3-63152eba188a', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-25 16:00:34.846226+00', ''),
	('00000000-0000-0000-0000-000000000000', '0eba094b-c1eb-4ae9-9ef0-3377dcdef4af', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 07:16:19.714544+00', ''),
	('00000000-0000-0000-0000-000000000000', '8bdcdca2-fb58-4ccf-8fc6-33c5dcd4ddff', '{"action":"token_revoked","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 07:16:19.71599+00', ''),
	('00000000-0000-0000-0000-000000000000', 'f2d0fd68-eb40-49d9-a65c-1cb6df9db568', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 07:16:19.871245+00', ''),
	('00000000-0000-0000-0000-000000000000', 'fb359985-7483-46ab-80ef-847ae6f2d019', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 09:49:17.342981+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a9e3cfdb-14fb-4019-b8ae-5a5546a0e575', '{"action":"token_revoked","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 09:49:17.344853+00', ''),
	('00000000-0000-0000-0000-000000000000', '7be915e0-47b7-404e-9a98-cd26bdfaab83', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 09:49:17.403855+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ed7aff62-a070-4667-9555-1112e79957de', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 12:29:57.774689+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b23c0149-5bc8-4183-b479-a34bf112bf59', '{"action":"token_revoked","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 12:29:57.775437+00', ''),
	('00000000-0000-0000-0000-000000000000', '00e9f887-0ed4-4268-a597-5bdabbc78cb6', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 12:29:57.800126+00', ''),
	('00000000-0000-0000-0000-000000000000', '9274b4dc-1629-4348-9af4-e2daacdaf774', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 15:56:16.292629+00', ''),
	('00000000-0000-0000-0000-000000000000', '73c40462-6dec-48f1-8af8-f83dcb3b6e55', '{"action":"token_revoked","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 15:56:16.296442+00', ''),
	('00000000-0000-0000-0000-000000000000', '071a23ff-42a9-4074-bc7f-1ffb927a1ee2', '{"action":"token_refreshed","actor_id":"39418e3b-0258-4452-af60-7acfcc1263ff","actor_username":"admin@quivr.app","actor_via_sso":false,"log_type":"token"}', '2024-06-26 15:56:16.675161+00', '');


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at", "is_anonymous") VALUES
	('00000000-0000-0000-0000-000000000000', '39418e3b-0258-4452-af60-7acfcc1263ff', 'authenticated', 'authenticated', 'admin@quivr.app', '$2a$10$vwKX0eMLlrOZvxQEA3Vl4e5V4/hOuxPjGYn9QK1yqeaZxa.42Uhze', '2024-01-22 22:27:00.166861+00', NULL, '', NULL, 'e91d41043ca2c83c3be5a6ee7a4abc8a4f4fa2afc0a8453c502af931', '2024-03-05 16:22:13.780421+00', '', '', NULL, '2024-06-24 21:00:12.94635+00', '{"provider": "email", "providers": ["email"]}', '{}', NULL, '2024-01-22 22:27:00.158026+00', '2024-06-26 15:56:16.302951+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false);


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."identities" ("provider_id", "user_id", "identity_data", "provider", "last_sign_in_at", "created_at", "updated_at", "id") VALUES
	('39418e3b-0258-4452-af60-7acfcc1263ff', '39418e3b-0258-4452-af60-7acfcc1263ff', '{"sub": "39418e3b-0258-4452-af60-7acfcc1263ff", "email": "admin@quivr.app", "email_verified": false, "phone_verified": false}', 'email', '2024-01-22 22:27:00.163787+00', '2024-01-22 22:27:00.163855+00', '2024-01-22 22:27:00.163855+00', '35f91d2f-db60-474c-8dd2-3fcbed9869bd');


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."sessions" ("id", "user_id", "created_at", "updated_at", "factor_id", "aal", "not_after", "refreshed_at", "user_agent", "ip", "tag") VALUES
	('a6aa5f22-f2cb-4927-86ac-65cda38812b1', '39418e3b-0258-4452-af60-7acfcc1263ff', '2024-06-24 21:00:12.946419+00', '2024-06-26 15:56:16.675546+00', NULL, 'aal1', NULL, '2024-06-26 15:56:16.675508', 'node', '192.168.48.1', NULL);


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."mfa_amr_claims" ("session_id", "created_at", "updated_at", "authentication_method", "id") VALUES
	('a6aa5f22-f2cb-4927-86ac-65cda38812b1', '2024-06-24 21:00:12.953007+00', '2024-06-24 21:00:12.953007+00', 'password', '47be428a-b0b1-4046-ba03-b1c83b0eade8');


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."refresh_tokens" ("instance_id", "id", "token", "user_id", "revoked", "created_at", "updated_at", "parent", "session_id") VALUES
	('00000000-0000-0000-0000-000000000000', 14, 'NxX7dcY3aWqry_WaBwX0Tg', '39418e3b-0258-4452-af60-7acfcc1263ff', true, '2024-06-24 21:00:12.948455+00', '2024-06-25 14:56:06.215705+00', NULL, 'a6aa5f22-f2cb-4927-86ac-65cda38812b1'),
	('00000000-0000-0000-0000-000000000000', 15, 'Qq3Mm9jsqP0aDpiI0tkX3w', '39418e3b-0258-4452-af60-7acfcc1263ff', true, '2024-06-25 14:56:06.21752+00', '2024-06-25 16:00:34.791993+00', 'NxX7dcY3aWqry_WaBwX0Tg', 'a6aa5f22-f2cb-4927-86ac-65cda38812b1'),
	('00000000-0000-0000-0000-000000000000', 16, '-ZqmC4HtcDyvNnZtqQRzDw', '39418e3b-0258-4452-af60-7acfcc1263ff', true, '2024-06-25 16:00:34.792856+00', '2024-06-26 07:16:19.716346+00', 'Qq3Mm9jsqP0aDpiI0tkX3w', 'a6aa5f22-f2cb-4927-86ac-65cda38812b1'),
	('00000000-0000-0000-0000-000000000000', 17, '0fogfQGgvHtJjUq1dMrdHA', '39418e3b-0258-4452-af60-7acfcc1263ff', true, '2024-06-26 07:16:19.716989+00', '2024-06-26 09:49:17.346493+00', '-ZqmC4HtcDyvNnZtqQRzDw', 'a6aa5f22-f2cb-4927-86ac-65cda38812b1'),
	('00000000-0000-0000-0000-000000000000', 18, 'W8rf6F2sb47F_lH6zH3QWg', '39418e3b-0258-4452-af60-7acfcc1263ff', true, '2024-06-26 09:49:17.347425+00', '2024-06-26 12:29:57.775952+00', '0fogfQGgvHtJjUq1dMrdHA', 'a6aa5f22-f2cb-4927-86ac-65cda38812b1'),
	('00000000-0000-0000-0000-000000000000', 19, 'A35SfN0jnpLWMW0a3T-HEA', '39418e3b-0258-4452-af60-7acfcc1263ff', true, '2024-06-26 12:29:57.776349+00', '2024-06-26 15:56:16.298189+00', 'W8rf6F2sb47F_lH6zH3QWg', 'a6aa5f22-f2cb-4927-86ac-65cda38812b1'),
	('00000000-0000-0000-0000-000000000000', 20, 'aAbsXYYlSALq14nwD2ubRQ', '39418e3b-0258-4452-af60-7acfcc1263ff', false, '2024-06-26 15:56:16.300071+00', '2024-06-26 15:56:16.300071+00', 'A35SfN0jnpLWMW0a3T-HEA', 'a6aa5f22-f2cb-4927-86ac-65cda38812b1');


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



--
-- Data for Name: api_brain_definition; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: api_keys; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: assistants; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: brain_subscription_invitations; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: brains_users; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: vectors; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: brains_vectors; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: chats; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: chat_history; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: composite_brain_connections; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: integrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."integrations" ("created_at", "integration_name", "integration_logo_url", "connection_settings", "id", "description", "integration_type", "max_files", "information", "tags", "allow_model_change", "integration_display_name", "onboarding_brain") VALUES
	('2024-03-06 21:21:07.251232+00', 'doc', 'https://quivr-cms.s3.eu-west-3.amazonaws.com/225911_200_46634039e4.png', NULL, 'b37a2275-61b3-460b-b4ab-94dfdf3642fb', 'Default description', 'custom', 5000, NULL, '{}', true, 'Brain', true),
	('2024-06-26 16:16:31.677998+00', 'gpt4', 'https://quivr-cms.s3.eu-west-3.amazonaws.com/1681038325chatgpt_logo_transparent_d0daa72d1c.png', NULL, 'daa6fde9-06cd-4a53-be81-6d379343c23c', 'GPT4', 'custom', 0, NULL, '{}', true, 'GPT4', false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."users" ("id", "email", "onboarded") VALUES
	('39418e3b-0258-4452-af60-7acfcc1263ff', 'admin@quivr.app', false);


--
-- Data for Name: integrations_user; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: knowledge; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: models; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."models" ("name", "price", "max_input", "max_output") VALUES
	('gpt-3.5-turbo-0125', 1, 10000, 1000),
	('gpt-4-0125-preview', 1, 4000, 4000);


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: onboardings; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: product_to_features; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."product_to_features" ("id", "models", "max_brains", "max_brain_size", "api_access", "stripe_product_id", "monthly_chat_credit") VALUES
	(1, '["gpt-3.5-turbo-1106"]', 1000, 50000000, false, 'prod_QIGYtKlFe8lhOc', 10000);


--
-- Data for Name: syncs_user; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: syncs_active; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: syncs_files; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: user_daily_usage; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: user_identity; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."user_identity" ("user_id", "openai_api_key", "company", "onboarded", "username", "company_size", "usage_purpose") VALUES
	('39418e3b-0258-4452-af60-7acfcc1263ff', NULL, 'Quivr', true, 'Quivr', NULL, '');


--
-- Data for Name: user_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."user_settings" ("user_id", "models", "max_brains", "max_brain_size", "is_premium", "api_access", "monthly_chat_credit", "last_stripe_check") VALUES
	('39418e3b-0258-4452-af60-7acfcc1263ff', '["gpt-3.5-turbo-0125", "gpt-4o"]', 1000, 50000000, false, false, 10000, NULL);


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 20, true);


--
-- Name: integrations_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."integrations_user_id_seq"', 7, true);


--
-- Name: product_to_features_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."product_to_features_id_seq"', 1, true);


--
-- Name: syncs_active_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."syncs_active_id_seq"', 1, true);


--
-- Name: syncs_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."syncs_files_id_seq"', 4, true);


--
-- Name: syncs_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."syncs_user_id_seq"', 1, true);


--
-- PostgreSQL database dump complete
--

RESET ALL;
