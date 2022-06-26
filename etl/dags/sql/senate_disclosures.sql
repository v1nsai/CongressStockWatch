CREATE TABLE IF NOT EXISTS senate_disclosures (
    file_date text not null,
    transaction_date text not null,
    issuer text not null,
    transaction_type text not null,
    transaction_hash text not null primary key
);