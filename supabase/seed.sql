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
	('00000000-0000-0000-0000-000000000000', 'f7fbe861-c477-483e-a74a-8dcb9f2df8c5', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"user_email":"admin@quivr.app","user_id":"bad271c8-973a-4dcc-8e87-1de818ea1234","user_phone":""}}', '2024-01-03 17:59:11.223649+00', '');


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at") VALUES
	('00000000-0000-0000-0000-000000000000', 'bad271c8-973a-4dcc-8e87-1de818ea1234', 'authenticated', 'authenticated', 'admin@quivr.app', '$2a$10$fo99ZlLdOex9QJy5cMN8OuQD2EBylfB1dPCfdLeXniDr6a6K1jOEu', '2024-01-03 17:59:11.22809+00', NULL, '', NULL, '', NULL, '', '', NULL, NULL, '{"provider": "email", "providers": ["email"]}', '{}', NULL, '2024-01-03 17:59:11.212675+00', '2024-01-03 17:59:11.228261+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL);


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



--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



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
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: onboardings; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."onboardings" ("user_id", "onboarding_a", "onboarding_b1", "onboarding_b2", "onboarding_b3", "creation_time") VALUES
	('bad271c8-973a-4dcc-8e87-1de818ea1234', true, true, true, true, '2024-01-03 17:59:11.212049');


--
-- Data for Name: stats; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: summaries; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: user_daily_usage; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: user_identity; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: user_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--



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

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 1, true);


--
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."documents_id_seq"', 1, false);


--
-- Name: stats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."stats_id_seq"', 1, false);


--
-- Name: summaries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."summaries_id_seq"', 1, false);


--
-- Name: vectors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."vectors_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

RESET ALL;
