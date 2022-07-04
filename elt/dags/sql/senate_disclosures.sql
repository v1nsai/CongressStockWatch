CREATE TABLE IF NOT EXISTS senate_disclosures (
    file_date text not null,
    transaction_date text not null,
    issuer text not null,
    transaction_type text not null,
    reporter text not null,
    amount text not null,
    ownership text not null,
    transaction_hash text not null,
    id serial primary key
);