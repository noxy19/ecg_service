CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
CREATE INDEX idx_username_hash ON users USING HASH (username);


CREATE TABLE ecgs (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    date_created timestamp NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE leads (
    ecg_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    number_of_samples INT,
    signal integer[] NOT NULL,
    PRIMARY KEY (name, ecg_id),
    FOREIGN KEY (ecg_id) REFERENCES ecgs(id)
);

CREATE TABLE insights (
    ecg_id UUID NOT NULL,
    lead_name VARCHAR(255) NOT NULL,
    crossings INT NOT NULL,
    PRIMARY KEY (ecg_id, lead_name),
    FOREIGN KEY (lead_name, ecg_id) REFERENCES leads(name, ecg_id),
    FOREIGN KEY (ecg_id) REFERENCES ecgs(id)
);