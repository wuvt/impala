CREATE TABLE track_metadata (
    id uuid NOT NULL PRIMARY KEY,
    added_by character varying NOT NULL,
    added_at timestamp without time zone NOT NULL,
    key character varying NOT NULL,
    value text NOT NULL,
    track_id uuid REFERENCES tracks(id) NOT NULL
);
