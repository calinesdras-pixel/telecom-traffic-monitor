CREATE TABLE IF NOT EXISTS abonnes (
    id BIGSERIAL PRIMARY KEY,
    numero VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(100),
    forfait_quota_mb NUMERIC(12,2) NOT NULL
        CHECK (forfait_quota_mb >= 0),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS applications (
    id BIGSERIAL PRIMARY KEY,
    nom VARCHAR(80) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS protocoles (
    id BIGSERIAL PRIMARY KEY,
    nom VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions_consommation (
    id BIGSERIAL PRIMARY KEY,

    abonne_id BIGINT NOT NULL
        REFERENCES abonnes(id),

    application_id BIGINT NOT NULL
        REFERENCES applications(id),

    protocole_id BIGINT NOT NULL
        REFERENCES protocoles(id),

    volume_mb NUMERIC(12,2) NOT NULL
        CHECK (volume_mb >= 0),

    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    ended_at TIMESTAMPTZ,

    CHECK (ended_at IS NULL OR ended_at >= started_at)
);
