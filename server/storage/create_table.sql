

CREATE TABLE IF NOT EXISTS snippets_table (
    snippet_uid UUID PRIMARY KEY UNIQUE,
    description VARCHAR(100),
    public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);