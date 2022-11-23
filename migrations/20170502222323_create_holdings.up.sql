CREATE TABLE formats (
    id uuid NOT NULL PRIMARY KEY,
    added_by character varying NOT NULL,
    added_at timestamp without time zone NOT NULL,
    name character varying NOT NULL,
    description text,
    physical boolean NOT NULL
);

CREATE TABLE stacks (
    id uuid NOT NULL PRIMARY KEY,
    added_by character varying NOT NULL,
    added_at timestamp without time zone NOT NULL,
    name character varying NOT NULL,
    description text
);

CREATE TABLE holding_groups (
    id uuid NOT NULL PRIMARY KEY,
    added_by character varying NOT NULL,
    added_at timestamp without time zone NOT NULL,
    album_title character varying NOT NULL,
    album_artist character varying NOT NULL,
    releasegroup_mbid uuid,
    description text,
    active boolean NOT NULL,
    stack_id uuid REFERENCES stacks(id) NOT NULL
);

CREATE TABLE holdings (
    id uuid NOT NULL PRIMARY KEY,
    added_by character varying NOT NULL,
    added_at timestamp without time zone NOT NULL,
    label character varying,
    release_mbid uuid,
    description text,
    source_url character varying,
    source_desc text,
    active boolean NOT NULL,
    holding_group_id uuid REFERENCES holding_groups(id) NOT NULL,
    format_id uuid REFERENCES formats(id) NOT NULL
);

CREATE TABLE rotation_releases (
    id uuid NOT NULL PRIMARY KEY,
    added_by character varying NOT NULL,
    added_at timestamp without time zone NOT NULL,
    start timestamp without time zone NOT NULL,
    stop timestamp without time zone,
    bin character varying,
    holding_id uuid REFERENCES holdings(id) NOT NULL
);
