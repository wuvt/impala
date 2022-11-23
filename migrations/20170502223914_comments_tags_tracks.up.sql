CREATE TYPE holdingcommenttype AS ENUM (
    'REVIEW',
    'COMMENT',
    'TRACK_WARNING',
    'OTHER'
);

CREATE TABLE holding_comments (
    id uuid NOT NULL PRIMARY KEY,
    added_by character varying NOT NULL,
    added_at timestamp without time zone NOT NULL,
    comment_text text,
    reviewer_username character varying,
    reviewer_fullname character varying NOT NULL,
    rating integer,
    review_date date,
    type holdingcommenttype NOT NULL,
    holding_id uuid REFERENCES holdings(id) NOT NULL
);

CREATE TABLE holding_tags (
    id uuid NOT NULL PRIMARY KEY,
    added_by character varying NOT NULL,
    added_at timestamp without time zone NOT NULL,
    owner character varying,
    tag character varying NOT NULL,
    holding_id uuid REFERENCES holdings(id) NOT NULL
);

CREATE TYPE trackfccstatus AS ENUM ('YES', 'NO', 'UNKNOWN');

CREATE TABLE tracks (
    id uuid NOT NULL PRIMARY KEY,
    added_by character varying NOT NULL,
    added_at timestamp without time zone NOT NULL,
    title character varying NOT NULL,
    artist character varying NOT NULL,
    file_path character varying,
    track_num integer NOT NULL,
    disc_num integer NOT NULL,
    track_mbid uuid,
    recording_mbid uuid,
    has_fcc trackfccstatus NOT NULL,
    holding_id uuid REFERENCES holdings(id) NOT NULL
);
