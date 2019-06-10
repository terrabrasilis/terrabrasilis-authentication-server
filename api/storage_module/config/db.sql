CREATE TABLE IF NOT EXISTS public.user
(
  id serial,
  email character varying(255) NOT NULL,
  password character varying(255) NOT NULL,
  registered_on timestamp without time zone NOT NULL,
  admin boolean NOT NULL DEFAULT false,
  verified boolean NOT NULL DEFAULT false,
  CONSTRAINT users_pkey PRIMARY KEY (id),
  CONSTRAINT users_email_key UNIQUE (email)
)
WITH (
  OIDS=FALSE
)
TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public.blacklist_token
(
  id serial,
  token character varying(500) NOT NULL,
  blacklisted_on timestamp without time zone NOT NULL,
  CONSTRAINT blacklist_tokens_pkey PRIMARY KEY (id),
  CONSTRAINT blacklist_tokens_token_key UNIQUE (token)
)
WITH (
  OIDS=FALSE
);