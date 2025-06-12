--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Ubuntu 14.18-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.18 (Ubuntu 14.18-0ubuntu0.22.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: analysis_summary; Type: TABLE; Schema: public; Owner: fintech_user
--

CREATE TABLE public.analysis_summary (
    id integer NOT NULL,
    bank_name character varying(50) NOT NULL,
    total_reviews integer NOT NULL,
    avg_sentiment_score double precision,
    theme_distribution jsonb,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.analysis_summary OWNER TO fintech_user;

--
-- Name: analysis_summary_id_seq; Type: SEQUENCE; Schema: public; Owner: fintech_user
--

CREATE SEQUENCE public.analysis_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.analysis_summary_id_seq OWNER TO fintech_user;

--
-- Name: analysis_summary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fintech_user
--

ALTER SEQUENCE public.analysis_summary_id_seq OWNED BY public.analysis_summary.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: fintech_user
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    review_text text NOT NULL,
    rating integer,
    review_date timestamp without time zone,
    bank_name character varying(50) NOT NULL,
    sentiment_label character varying(20),
    sentiment_score double precision,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT reviews_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.reviews OWNER TO fintech_user;

--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: fintech_user
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_id_seq OWNER TO fintech_user;

--
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fintech_user
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- Name: themes; Type: TABLE; Schema: public; Owner: fintech_user
--

CREATE TABLE public.themes (
    id integer NOT NULL,
    review_id integer,
    theme_name character varying(50) NOT NULL,
    confidence_score double precision,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.themes OWNER TO fintech_user;

--
-- Name: themes_id_seq; Type: SEQUENCE; Schema: public; Owner: fintech_user
--

CREATE SEQUENCE public.themes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.themes_id_seq OWNER TO fintech_user;

--
-- Name: themes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fintech_user
--

ALTER SEQUENCE public.themes_id_seq OWNED BY public.themes.id;


--
-- Name: analysis_summary id; Type: DEFAULT; Schema: public; Owner: fintech_user
--

ALTER TABLE ONLY public.analysis_summary ALTER COLUMN id SET DEFAULT nextval('public.analysis_summary_id_seq'::regclass);


--
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: fintech_user
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- Name: themes id; Type: DEFAULT; Schema: public; Owner: fintech_user
--

ALTER TABLE ONLY public.themes ALTER COLUMN id SET DEFAULT nextval('public.themes_id_seq'::regclass);


--
-- Name: analysis_summary analysis_summary_bank_name_key; Type: CONSTRAINT; Schema: public; Owner: fintech_user
--

ALTER TABLE ONLY public.analysis_summary
    ADD CONSTRAINT analysis_summary_bank_name_key UNIQUE (bank_name);


--
-- Name: analysis_summary analysis_summary_pkey; Type: CONSTRAINT; Schema: public; Owner: fintech_user
--

ALTER TABLE ONLY public.analysis_summary
    ADD CONSTRAINT analysis_summary_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: fintech_user
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: themes themes_pkey; Type: CONSTRAINT; Schema: public; Owner: fintech_user
--

ALTER TABLE ONLY public.themes
    ADD CONSTRAINT themes_pkey PRIMARY KEY (id);


--
-- Name: reviews_bank_name_idx; Type: INDEX; Schema: public; Owner: fintech_user
--

CREATE INDEX reviews_bank_name_idx ON public.reviews USING btree (bank_name);


--
-- Name: reviews_sentiment_label_idx; Type: INDEX; Schema: public; Owner: fintech_user
--

CREATE INDEX reviews_sentiment_label_idx ON public.reviews USING btree (sentiment_label);


--
-- Name: themes_review_id_idx; Type: INDEX; Schema: public; Owner: fintech_user
--

CREATE INDEX themes_review_id_idx ON public.themes USING btree (review_id);


--
-- Name: themes_theme_name_idx; Type: INDEX; Schema: public; Owner: fintech_user
--

CREATE INDEX themes_theme_name_idx ON public.themes USING btree (theme_name);


--
-- Name: themes themes_review_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fintech_user
--

ALTER TABLE ONLY public.themes
    ADD CONSTRAINT themes_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.reviews(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

