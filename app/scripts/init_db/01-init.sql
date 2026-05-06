CREATE EXTENSION IF NOT EXISTS postgis;


CREATE TABLE IF NOT EXISTS vacancies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    vacancy_name TEXT NOT NULL,
    vacancy_type INTEGER NOT NULL,
    vacancy_link TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    visibility SMALLINT DEFAULT 0,

    tags TEXT[],
    hash TEXT UNIQUE NOT NULL
);

CREATE INDEX idx_vacancies_id ON vacancies(id);


CREATE TABLE IF NOT EXISTS spatial_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    location_name TEXT NOT NULL,

    geom GEOMETRY(MultiPolygon, 4326) NOT NULL,

    vacancy_id UUID NOT NULL,
    CONSTRAINT fk_spatial_data_provider
        FOREIGN KEY (vacancy_id)
        REFERENCES vacancies(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_spatial_data_geom ON spatial_info USING GIST (geom);
CREATE INDEX idx_spatial_data_id ON spatial_info(vacancy_id);

COMMENT ON TABLE spatial_info IS 'QGIS geo-objects table';
COMMENT ON COLUMN spatial_info.geom IS 'WGS84';


CREATE TABLE IF NOT EXISTS providers_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    provider_name TEXT NOT NULL UNIQUE,
    link TEXT,
    registered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS tags (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    tag_name TEXT UNIQUE NOT NULL,
    tag_count BIGINT DEFAULT 0
);


CREATE TABLE IF NOT EXISTS vacancies_tags (
    vacancy_id UUID REFERENCES vacancies(id) ON DELETE CASCADE,
    tag_id BIGINT REFERENCES tags(id) ON DELETE CASCADE,

    PRIMARY KEY (vacancy_id, tag_id)
);


CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name TEXT NOT NULL,

    admin BOOLEAN DEFAULT FALSE,
    rights INTEGER DEFAULT 1,

    telegram_id INTEGER UNIQUE NOT NULL,
    telegram_name TEXT,

    email TEXT UNIQUE,
    phone_number TEXT UNIQUE
);

CREATE INDEX idx_users_id ON users(id)
