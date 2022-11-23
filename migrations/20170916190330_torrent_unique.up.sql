ALTER TABLE holdings
    ADD CONSTRAINT holdings_torrent_hash_key UNIQUE (torrent_hash);