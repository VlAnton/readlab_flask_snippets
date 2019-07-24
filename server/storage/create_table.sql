CREATE TABLE snippets_table (
    snippet_uid UUID PRIMARY KEY UNIQUE,
    description VARCHAR(100),
    public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE file (
    file_id SERIAL,
    content TEXT NOT NULL,
    lang VARCHAR(50) NOT NULL,
    snippet_uid UUID REFERENCES snippets_table(snippet_uid)
);