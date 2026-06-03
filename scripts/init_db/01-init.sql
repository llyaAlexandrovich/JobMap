CREATE TABLE IF NOT EXISTS spatial_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_name TEXT NOT NULL,
    geom GEOMETRY(Point, 4326) NOT NULL
);
CREATE INDEX idx_spatial_data_geom ON spatial_info USING GIST (geom);
COMMENT ON TABLE spatial_info IS 'QGIS geo-objects table';
COMMENT ON COLUMN spatial_info.geom IS 'WGS84';

CREATE TABLE IF NOT EXISTS providers_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_name TEXT NOT NULL UNIQUE,
    provider_link TEXT,
    registered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tag_name TEXT UNIQUE NOT NULL,
    tag_count BIGINT DEFAULT 0
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
CREATE INDEX idx_users_id ON users(id);


CREATE TABLE IF NOT EXISTS companies_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL UNIQUE,
    company_location UUID REFERENCES spatial_info(id) ON DELETE CASCADE,
    company_link TEXT,
    company_rating SMALLINT DEFAULT 100
);
CREATE INDEX idx_companies_info_id ON companies_info(id);


CREATE TABLE IF NOT EXISTS vacancies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vacancy_name TEXT NOT NULL,
    vacancy_type INTEGER NOT NULL,
    vacancy_link TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    visibility SMALLINT DEFAULT 0,
    hash TEXT UNIQUE NOT NULL,
    location UUID NOT NULL,
    company UUID NOT NULL,
    
    CONSTRAINT fk_spatial_info
        FOREIGN KEY (location)
        REFERENCES spatial_info(id)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_company_info
        FOREIGN KEY (company)
        REFERENCES companies_info(id)
        ON DELETE CASCADE
);
CREATE INDEX idx_vacancies_id ON vacancies(id);


CREATE TABLE IF NOT EXISTS vacancies_tags (
    vacancy_id UUID REFERENCES vacancies(id) ON DELETE CASCADE,
    tag_id BIGINT REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (vacancy_id, tag_id)
);
