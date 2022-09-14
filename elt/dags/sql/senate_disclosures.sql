CREATE SCHEMA IF NOT EXISTS congress;

CREATE TABLE IF NOT EXISTS congress.senate_disclosures (
    id serial primary key not null,
    first_name varchar not null,
    last_name varchar not null,
    filer_type varchar not null,
    report_type varchar not null,
    date_received varchar not null
);